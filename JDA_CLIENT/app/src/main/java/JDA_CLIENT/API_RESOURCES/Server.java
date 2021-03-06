package JDA_CLIENT.API_RESOURCES;

import org.json.simple.JsonObject;

import JDA_CLIENT.Main;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.Permission;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.exceptions.PermissionException;
import net.dv8tion.jda.api.entities.Member;

import java.util.ArrayList;
import java.util.Collection;
import java.util.concurrent.TimeUnit;

import javax.annotation.Nullable;

/**
 * This class is the representation of a discord server. It also is an ApiResource, which is why it
 * implements that interface and its methods.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class Server implements ApiResource { //Could make it extend JDA Guild object?
    /** 
     * This is the ID of the server. It corresponds to the one given by discord, which is why it
     * is a long isntead of just being an int.
     */
    private long ID;
    /** This is the list of muted users on the server. */
    private ArrayList<Long> mutedUsers;
    /** This is the role to give to muted users. */
    private long mutedRoleId;
    /** This is the default time before the user is allowed to speak again (in hours : max 672) */
    private long mutedCooldown;
    /** This is the amount of warn needed before the user gets banned. */
    private int maxWarn;
    /** This is the cooldown time in days before a warned user loses one warn. */
    private int cooldown;
    /** This is the list of users banned from the server. Can be empty. */
    private ArrayList<Long> banned;
    /** This is the list of warnings linked to this server. Can be empty. */
    private ArrayList<Long> warnings;
    /** This is the prefix used to recognized a custom command. */
    private String prefix;
    /** This is the list of roles to give to a user joining the server. Can be empty. */
    private ArrayList<Role> autoRoles;
    /** This is the list of reaction roles linked to this server. Can be empty. */
    private ArrayList<Long> reactionRoles;
    /** This is the list of custom commands linked to this server. Can be empty. */
    private ArrayList<Long> customCommands;

    /**
     * This is the list of warning objects for this server. It is not necessarily synchronized with
     * the warnings array list, which is why it has to be manipulated carefully.
     * The objects within this list are the same as the ones in the memory (in the Main class), as
     * they will contain their reference. Therefore, if we want to delete an item in memory (which
     * occurs when we load a new one), we NEED to call the method vanishWarning(int index), that
     * will destroy the reference to this object by removing it's use in this list.
     * 
     * Note that the call to the afore mentioned method will NOT affect the warnings array list. It
     * simply aims to eliminate the object from the memory, not to change the data.
     */
    //private ArrayList<Warning> dynWarnings;

    /** This is the Guild instance it is linked to. */
    private Guild JDAServer;

    /**
     * This constructor of Server is the one that will be called when the server is first created.
     * It mustn't be called if ther Server already exists in the API!
     * 
     * @param server The Guild instance to which the created Server instance will be linked to.
     */
    public Server(Guild server) {
        //As these data do not depend on the user, I'm gonna be optimistic and consider them as
        //correct without verifying.
        this.ID = server.getIdLong();
        this.JDAServer = server;

        //And we initialize the attributes with default values.
        this.mutedUsers = new ArrayList<Long>();
        this.mutedCooldown = Main.serverDefaultMutedCooldown;
        this.maxWarn = Main.serverDefaultMaxWarn;
        this.cooldown = Main.serverDefualtCooldown;
        this.banned = new ArrayList<Long>();
        this.warnings = new ArrayList<Long>();
        this.prefix = Main.serverDefaultPrefix;
        this.autoRoles = new ArrayList<Role>();
        this.reactionRoles = new ArrayList<Long>();
        this.customCommands = new ArrayList<Long>();
    }

    /**
     * This constructor of Server is the one that will be called when the server is retrieved from
     * the API. Which is why we create it from a json dataset.
     * 
     * @param jda The bot JDA. This is mandatory because without it we can't retrieve the autoRole.
     * @param server The JsonObject retrieved from the API via a GET HTTP request.
     */
    public Server(JDA jda, JsonObject server) {
        //At first we create the collections
        Collection<Long> mutedUsersCollection = (Collection<Long>) server.getCollection("mutedUsers");
        Collection<Long> bannedCollection = (Collection<Long>) server.getCollection("banned");
        Collection<Long> warningsCollection = (Collection<Long>) server.getCollection("warnings");
        Collection<Long> autoRolesCollection = (Collection<Long>) server.getCollection("autoRoles");
        Collection<Long> reactionRolesCollection = (Collection<Long>) server.getCollection("reactionRoles");
        Collection<Long> customCommandsCollection = (Collection<Long>) server.getCollection("customCommands");

        //Then we parse the simple arguments
        this.ID = server.getLong("ID");
        this.JDAServer = jda.getGuildById(this.ID); //Thanks to that line we can get the Roles.
        this.mutedRoleId = server.getLong("mutedRole");
        this.mutedCooldown = server.getLong("mutedCooldown");
        this.maxWarn = server.getInteger("maxWarn");
        this.cooldown = server.getInteger("cooldown");
        this.prefix = server.getString("prefix");

        //And finally we initialize the arrays and add the content of the mathcing collection.
        this.mutedUsers = new ArrayList<Long>(mutedUsersCollection);
        this.banned = new ArrayList<Long>(bannedCollection);
        this.warnings = new ArrayList<Long>(warningsCollection);
        //This one is treated a bit differently as we have to retrieve all the objects form their ID.
        this.autoRoles = new ArrayList<Role>();
        for (Long l : autoRolesCollection) {
            this.autoRoles.add(this.JDAServer.getRoleById(l));
        }
        this.reactionRoles = new ArrayList<Long>(reactionRolesCollection);
        this.customCommands = new ArrayList<Long>(customCommandsCollection);
    }

    /**
     * This method will have to be called by the MuteUser command after parsing the sender's
     * mesage. It will basically execute the actions to make the sentence effective.
     * 
     * @param originMember The member at the origin of the call. Should be
     *                     this.JDAServer.getSelfMember() if it is the bot itself.
     * @param affectedMember The member to mute. Won't accept it as an Id (long).
     * @param time The amount of hours the user will be muted on the server. If the sender didn't
     *             specify anything for it, the value 0 will have to be passed, which will make the
     *             method use the server's default value.
     * 
     * @throws PermissionException When the bot can't perform the action because he doesn't have
     *                             the permissions for it, or when the member at the origin of the
     *                             call doesn't have it either.
     * 
     * @return The amount of time, as a long, for which the specified user's been muted. Useful for
     *         the success output message.
     */
    public long muteUser(Member originMember, Member affectedMember, long time) throws PermissionException {
        //First we have to give the user the muted role if it exists
        Role mutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

        if (!originMember.hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.memberManageRolesPermissionLack);
        }

        //This works because if the role we look for can't be found, the getRoleById method reurns
        //a null Role.
        if (mutedRole != null) {
            if (this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
                this.JDAServer.addRoleToMember(affectedMember, mutedRole);
            } else {
                throw new PermissionException(Main.english.selfManageRolesPermissionLack);
            }
        }

        //Note that the muted role can intentionally not be set, and on top of that, that role can
        //be just a label, so we have to timeout the user using discord functions.
        //In order to do that, we simply check the bot's permissions and throw a PermissionException
        //if it doesn't have the required permissions.
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.selfModerateMembersPermissionLack);
        }

        //This could be in a else statement, but as the throw Exception makes the method return, it
        //isn't mandatory.
        if (time <= 0 || time > 672) { //If the provided cooldown is wrong, default value is used.
            affectedMember.timeoutFor(this.mutedCooldown, TimeUnit.HOURS);
            //Then we add the user to the muted list.
            this.mutedUsers.add(affectedMember.getIdLong());

            //And we return the mutedCooldown to tell the calling method how long the user has been
            //muted for.
            return this.mutedCooldown;
        } else {
            affectedMember.timeoutFor(time, TimeUnit.HOURS);
            //Same here, but we return time instead.
            this.mutedUsers.add(affectedMember.getIdLong());
            return time;
        }
    }

    /**
     * This method will have to be called by the UnmuteUser command after parsing the sender's
     * mesage. It will basically execute the actions to revoque the sentence.
     * 
     * @param originMember The member at the origin of the call. Should be
     *                     this.JDAServer.getSelfMember() if it is the bot itself.
     * @param affectedMember The member to unmute. Won't accept it as an Id (long).
     * 
     * @throws PermissionException When the bot can't perform the action because he doesn't have
     *                             the permissions for it, or when the member at the origin of the
     *                             call doesn't have it either.
     */
    public void unmuteUser(Member originMember, Member affectedMember) throws PermissionException {
        //Just like the muteUser method, we're gonna check if there is a role attributed to muted
        //users. If so, we will need to make sure the bot has the right permissions to edit the
        //user's role, and then remove that role.

        Role mutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

        //As our goal is not to make everyone able to manage the server, we need to verify the
        //member at the origin of the call is allowed to to what he asks the bot to do.
        if (!originMember.hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.memberManageRolesPermissionLack);
        }

        //Again, this works because if the role we look for can't be found, the getRoleById method
        //returns a null role.
        if (mutedRole != null) {
            if (this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
                this.JDAServer.removeRoleFromMember(affectedMember, mutedRole);
            } else {
                throw new PermissionException(Main.english.selfManageRolesPermissionLack);
            }
        }

        //Now that the role is removed if there was one, we need to revoque the user's timeout.
        //Let's check permissions once again and then act if possible :
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.selfModerateMembersPermissionLack);
        }

        //Finally, we remove the user's timeout.
        affectedMember.removeTimeout();
        //And we remove the user from the muted list.
        this.mutedUsers.remove(affectedMember.getIdLong());
    }

    /**
     * This method aims to change the muted role of the server. Note that this method can also be
     * used for removing the muted role. For that you simply have to give it a value that doesn't
     * correspond to any role in the concerned server.
     * 
     * @param originMember The member at the origin of the call. Should be
     *                     this.JDAServer.getSelfMember() if it is the bot itself.
     * @param mutedRoleId The id of the new role for muted members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions. Could be caught
     *                             but I prefer to let it get up to the call of this method to make
     *                             sure the output is send to the user.
     */
    public void setMutedRole(Member originMember, long mutedRoleId) throws PermissionException {
        //This might actually sound werid because the muted role is stored via its id, but this
        //method will simply call its overload with a Role as a parameter, as we have to verify
        //whether the id given corresponds to any existing role or not.

        //Reasons behind that are that we want the muted users to change roles if the role is
        //modified and to remove the role from them if it is changed to an invalid one. Please see
        //the setMutedRole(Role mutedRole) method for a more accurate explanation of this.
        Role mutedRole = JDAServer.getRoleById(mutedRoleId);
        setMutedRole(originMember, mutedRole);
    }

    /**
     * This method aims to change the muted role of the server. Note that this method can also be
     * used for removing the muted role. For that you simply have to give it a null Role.
     * 
     * @param originMember The member at the origin of the call. Should be
     *                     this.JDAServer.getSelfMember() if it is the bot itself.
     * @param mutedRole The new role for muted members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions. Could be caught
     *                             but I prefer to let it get up to the call of this method to make
     *                             sure the output is send to the user.
     */
    public void setMutedRole(Member originMember, Role mutedRole) throws PermissionException {
        //Here we have two possibilities :
        //1 : The Role given is null and we need to remove the muted role from the muted users
        //2 : The Role given is existing, which means we have to change it for all muted users
        
        if (mutedRole != null) {
            //Case 2 :

            //First, let's just check that the member at the origin of the call has the right perms!
            if (!originMember.hasPermission(Permission.MANAGE_SERVER)) {
                throw new PermissionException(Main.english.memberManageServerPermissionLack);
            }

            //We retrieve the role previously applied.
            Role previousMutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

            //And we check its value:
            //If it was null, we just have to add the new role
            if (previousMutedRole == null) {
                addRoleToMembers(this.mutedUsers, mutedRole);
            }
            //If it was different to the new one, we have to add the new role and remove the old.
            else if (!previousMutedRole.equals(mutedRole)) {
                exchangeRoleOnMembers(this.mutedUsers, previousMutedRole, mutedRole);
            }
            //No else 'cause it would only be reached when it is the same as the one it was before,
            //meaning there is just nothing to do.

            this.mutedRoleId = mutedRole.getIdLong();

        } else {
            //Case 1 : We let the removeMutedRole method handle it to avoid duplicating code.
            removeMutedRole(originMember);
        }
    }

    /**
     * A getter, as basic as it can get. It gives the id of the muted role on this server. This
     * doesn't give any insurance towards the existence of a role corresponding to the Id it
     * returns!
     * 
     * @return The id of the muted role.
     */
    public long getMutedRoleId() {
        return this.mutedRoleId;
    }

    /**
     * This method returns the role associated to mutedUsers. Notice that it will return a null
     * value if there is no role associated, or if it is incorrect (if it has been deleted for
     * instance).
     * 
     * @return The role associated to mutedUsers.
     */
    @Nullable
    public Role getMutedRole() {
        return this.JDAServer.getRoleById(this.mutedRoleId);
    }

    /**
     * This method aims to remove the muted role of the server. It works by simply putting it at 0
     * and removing previous roles (if there was one) from the mutedMembers.
     * 
     * @param originMember The member at the origin of the call. Should be
     *                     this.JDAServer.getSelfMember() if it is the bot itself.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions. Could be caught
     *                             but I prefer to let it get up to the call of this method to make
     *                             sure the output is send to the user.
     */
    public void removeMutedRole(Member originMember) throws PermissionException {
        //We retrieve the role previously applied.
        Role previousMutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

        //We make sure the member calling has the right permissions
        if (!originMember.hasPermission(Permission.MANAGE_SERVER)) {
            throw new PermissionException(Main.english.memberManageServerPermissionLack);
        }

        if (previousMutedRole != null) {
            removeRoleFromMembers(this.mutedUsers, previousMutedRole);
        }

        //In the end, we give a 0 value to the mutedRole.
        this.mutedRoleId = 0;
    }

    /**
     * This method modifies the server's default muted cooldown to the one given as a parameter.
     * Before we do that, we, of course, ensure that the member at the origin of the command has
     * the adequate permissions, and that the given time is correct.
     * 
     * @param member The member at the origin of the change. If it is the bot itself, then this
     *               member should be : this.JDAServer.getSelfMember().
     * @param time The new defualt cooldown time when muting users. Should be between 1 and 672.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     * @throws IllegalArgumentException When the time given is whether too low or too high.
     */
    public void setMutedCooldown(Member member, long time) throws PermissionException, IllegalArgumentException {
        //First of all, we need to check the user's rights, to ensure he's allowed to permform this
        //action.
        if (!member.hasPermission(Permission.MANAGE_SERVER)) {
            throw new PermissionException(Main.english.memberManageServerPermissionLack);
        }

        //As the time needs to be between 1 and 672, and could be provided by a user, I need to
        //make sure the time is correct.
        if (time > 672) {
            throw new IllegalArgumentException(Main.english.mutedCooldownTooHigh);
        } else if (time <= 0) {
            throw new IllegalArgumentException(Main.english.mutedCooldownTooLow);
        }

        this.mutedCooldown = time;
    }

    /**
     * A simple getter that returns the cooldown time before muted users can speak again.
     * 
     * @return The time, in hours, of the default cooldown.
     */
    public long getMutedCooldown() {
        return this.mutedCooldown;
    }

    /**
     * This method will make a call to the setMutedCooldown method, with the default value for
     * cooldown.
     * 
     * @param member The member at the origin of the change. If it is the bot itself, then this
     *               member should be : this.JDAServer.getSelfMember().
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void resetMutedCooldown(Member member) throws PermissionException {
        setMutedCooldown(member, Main.serverDefaultMutedCooldown);
    }

    /**
     * This method changes the server's maximum warning amount before the ban to the given value.
     * Before we do that, we, of course, ensure that the member at the origin of the command has
     * the adequate permissions, and that the given amount is correct.
     * Once changed to a lower amount, we'll have to check the whole list of warned members to
     * make sure none of them gets away with more warnings than they should be allowed. This option
     * will of course be deactivable.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * @param amount The new amount of warnings before the ban. Should be 1 or higher.
     * @param retroActive Whether we should control the whole list if the amount is reduced.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     * @throws IllegalArgumentException When the amount is below 1.
     */
    public void setMaxWarn(Member originMember, int amount, boolean retroActive) throws PermissionException, IllegalArgumentException {
        int previousAmount;

        //First of all, we need to check the user's rights, to ensure he's allowed to permform this
        //action.
        if (!originMember.hasPermission(Permission.MANAGE_SERVER)) {
            throw new PermissionException(Main.english.memberManageServerPermissionLack);
        }

        //As the amount needs to be greater than 0, and could be provided by a user, I need to make
        //sure it is correct.
        if (amount < 1) {
            throw new IllegalArgumentException(Main.english.maxWarningAmountTooLow);
        }

        previousAmount = this.maxWarn;
        this.maxWarn = amount;

        //And finally, if the command is retroActive, and the amount lower than the previous one,
        //we start a global checkup.
        if (retroActive && previousAmount > amount) {
            checkWarningAmounts();
        }
    }

    /**
     * A simple getter that returns the amount of warnings before users gets banned.
     * 
     * @return The maximum amount of warning set for this server.
     */
    public int getmaxWarn() {
        return this.maxWarn;
    }

    /**
     * This method will make a call to the setMaxWarn method, with the default value for warnings.
     * 
     * @param member The member at the origin of the change. If it is the bot itself, then this
     *               member should be : this.JDAServer.getSelfMember().
     * @param retroActive Whether we should control the whole list if the amount is reduced.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void resetMaxWarn(Member member, boolean retroActive) throws PermissionException {
        setMaxWarn(member, Main.serverDefaultMaxWarn, retroActive);
    }

    /**
     * A simple getter that returns the amount of time before users loses one warning.
     * 
     * @return The cooldown in days for warnings to reduce.
     */
    public int getCooldown() {
        return this.cooldown;
    }

    /**
     * This method changes the server's cooldown before the warned users loses one warn. Before we
     * do that, we, of course, ensure that the member at the origin of the command has the adequate
     * permissions, and that the given time is correct.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * @param time The new amount of days before the reduction of warnings. If it is below 1, the
     *             disableCooldown() method will be called instead (puting at 0).
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void setCooldown(Member originMember, int time) throws PermissionException {
        //So first we check the time, in order not to make the member verifications twice.
        if (time < 1) {
            disableCooldown(originMember);

        //Otherwise we check the member's rights and act in function.
        } else {
            if (!originMember.hasPermission(Permission.MANAGE_SERVER)) {
                throw new PermissionException(Main.english.memberManageServerPermissionLack);
            }

            this.cooldown = time;
        }
    }

    /**
     * This method will make a call to the setCooldown method, with the default value for cooldown.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void resetCooldown(Member originMember) throws PermissionException {
        setCooldown(originMember, Main.serverDefualtCooldown);
    }

    /**
     * This method disables the server's cooldown before the warned users loses one warn. Before we
     * do that, we, of course, ensure that the member at the origin of the command has the adequate
     * permissions.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void disableCooldown(Member originMember) throws PermissionException {
        //First we check that the member's rigths are adequate
        if (!originMember.hasPermission(Permission.MANAGE_SERVER)) {
            throw new PermissionException(Main.english.memberManageServerPermissionLack);
        }

        this.cooldown = 0;
    }

    /**
     * This method will make a call to the resetCooldown method. It's not yet particularly useful
     * but it could become useful in the future if I decide to disable/enable the cooldown via a
     * boolean attribute instead of setting the cooldown value.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void enableCooldown(Member originMember) throws PermissionException {
        resetCooldown(originMember);
    }

    /**
     * This method will send back the whole list of banned members on this server.
     * 
     * @return An ArrayList of Long objects, containing all the IDs of banned members.
     */
    public ArrayList<Long> getBannedList() {
        return this.banned;
    }

    /**
     * This method is an override of the ArrayList get(int index) method.
     * 
     * @param index The index of the object to search in the list.
     * 
     * @return The long ID of the member at the index given, or 0 if there was none.
     */
    public long getBannedMember(int index) {
        long memberId;
        try {
            memberId = this.banned.get(index);
        } catch (IndexOutOfBoundsException e) {
            memberId = 0;
        }

        return memberId;
    }

    /**
     * This method is an override of the ArrayList's indexOf(Object o). It aims to return the index
     * of the given element in the list.
     * 
     * @param memberId The ID (as a long) of the member to look for.
     * 
     * @return The index of the given element or -1 if it is not found in the list.
     */
    public int getBannedMemberIndex(long memberId) {
        return this.banned.indexOf(memberId);
    }

    /**
     * This method is an override of the ArrayList's indexOf(Object o). It aims to return the index
     * of the given element in the list.
     * 
     * @param member The member to look for.
     * 
     * @return The index of the given element or -1 if it is not found in the list.
     */
    public int getBannedMemberIndex(Member member) {
        return this.banned.indexOf(member.getIdLong());
    }

    /**
     * This method's purpose is to tell whether the given element appears in the list ; and is
     * therefore banned or not. It is essentially an override of the ArrayList's contains(Object o)
     * method.
     * 
     * @param memberId The ID (as a long) of the member to look for.
     * 
     * @return True if the ID is found in the list, else false.
     */
    public boolean isMemberBanned(long memberId) {
        return this.banned.contains(memberId);
    }

    /**
     * This method's purpose is to tell whether the given element appears in the list ; and is
     * therefore banned or not. It is essentially an override of the ArrayList's contains(Object o)
     * method.
     * 
     * @param member The member to look for.
     * 
     * @return True if the member's ID is found in the list, else false.
     */
    public boolean isMemberBanned(Member member) {
        return this.banned.contains(member.getIdLong());
    }

    /**
     * This method will add a member to the banned members list. It'll check the rights of the
     * member that asked for it to make sure he/she is allowed to do such a thing.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * @param memberId The ID in a long shape of the member to add to the banned list.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void addBannedMember(Member originMember, long memberId) throws PermissionException {
        if (!originMember.hasPermission(Permission.BAN_MEMBERS)) {
            throw new PermissionException(Main.english.memberBanMembersPermissionLack);
        }

        this.banned.add(memberId);
    }

    /**
     * This method will add a member to the banned members list. It'll check the rights of the
     * member that asked for it to make sure he/she is allowed to do such a thing.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * @param member The member member to add to the banned list.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void addBannedMember(Member originMember, Member member) throws PermissionException {
        if (!originMember.hasPermission(Permission.BAN_MEMBERS)) {
            throw new PermissionException(Main.english.memberBanMembersPermissionLack);
        }

        this.banned.add(member.getIdLong());
    }

    /**
     * This method will remove a member from the banned members list. It'll check the rights of the
     * member that asked for it to make sure he/she is allowed to do such a thing.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * @param memberId The ID in a long shape of the member to remove from the banned list.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void removeBannedMember(Member originMember, long memberId) throws PermissionException {
        if (!originMember.hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.memberModerateMembersPermissionLack);
        }

        this.banned.remove(memberId);
    }

    /**
     * This method will remove a member from the banned members list. It'll check the rights of the
     * member that asked for it to make sure he/she is allowed to do such a thing.
     * 
     * @param originMember The member at the origin of the change. If it is the bot itself, then
     *                     this member should be : this.JDAServer.getSelfMember().
     * @param member The member to remove from the banned list.
     * 
     * @throws PermissionException When the member who is at the origin of the call doesn't have
     *                             the adequate permissions.
     */
    public void removeBannedMember(Member originMember, Member member) throws PermissionException {
        if (!originMember.hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.memberModerateMembersPermissionLack);
        }

        this.banned.remove(member.getIdLong());
    }

    /**
     * This method will send back the whole list of warnings for this server.
     * 
     * @return An ArrayList of Long objects, containing all the IDs of the warnings.
     */
    public ArrayList<Long> getWarningList() {
        return this.warnings;
    }

    /**
     * This method is an override of the ArrayList get(int index) method.
     * 
     * @param index The index of the object to search in the list.
     * 
     * @return The long ID of the warning at the index given, or 0 if there was none.
     */
    public long getWarning(int index) {
        long warningId;
        try {
            warningId = this.warnings.get(index);
        } catch (IndexOutOfBoundsException e) {
            warningId = 0;
        }

        return warningId;
    }

    /**
     * This method is an override of the ArrayList's indexOf(Object o). It aims to return the index
     * of the given element in the list.
     * 
     * @param warningId The ID (as a long) of the warning to look for.
     * 
     * @return The index of the given element or -1 if it is not found in the list.
     */
    public int getWarningIndex(long warningId) {
        return this.warnings.indexOf(warningId);
    }

    ///** TO UNCOMMENT WHEN WARNINGS DONE!
    // * This method is an override of the ArrayList's indexOf(Object o). It aims to return the index
    // * of the given element in the list.
    // * 
    // * @param warning The warning to look for.
    // * 
    // * @return The index of the given element or -1 if it is not found in the list.
    // */
    //public int getWarningIndex(Warning warning) {
    //    return this.warnings.indexOf(warning.getId());
    //}

    /**
     * This method's purpose is to tell whether the given element appears in the list ; and is
     * therefore affiliated with this server or not. It is essentially an override of the
     * ArrayList's contains(Object o) method.
     * 
     * @param warningId The ID (as a long) of the warning to look for.
     * 
     * @return True if the ID is found in the list, else false.
     */
    public boolean isWarningAffiliated(long warningId) {
        return this.warnings.contains(warningId);
    }

    ///** TO UNCOMMENT WHEN WARNINGS DONE!
    // * This method's purpose is to tell whether the given element appears in the list ; and is
    // * therefore affiliated with this server or not. It is essentially an override of the
    // * ArrayList's contains(Object o) method.
    // * 
    // * @param warning The warning to look for.
    // * 
    // * @return True if the warning's ID is found in the list, else false.
    // */
    //public boolean isWarningAffiliated(Warning warning) {
    //    return this.warnings.contains(warning.getId());
    //}
    
    ///**
    // * This method's purpose is to return the Warning object concerning the given member. To do so,
    // * it will run through the list of warnings of this server.
    // * 
    // * @param memberId The ID as a long of the member that we want to find the warning of.
    // */
    //public Warning getMemberWarning(long memberId) {
    //    //First step is to ensure we have all the server's warnings in memory.
    //    retrieveWarnings();
    //
    //    //Then we iterate through the ones that belongs to this server, looking for one which user
    //    //ID matches the one of the user.
    //    for (Warning warning : dynWarnings) {
    //        //Not so good looking but very clear
    //        if (warning.getUser() == memberId) {
    //            return warning;
    //        }
    //    }
    //}

    ///**
    // * This method's purpose is to return the Warning object concerning the given member. To do so,
    // * it will run through the list of warnings of this server.
    // * 
    // * @param member The member that we want to find the warning of.
    // */
    //public Warning getMemberWarning(Member member) {
    //    //First step is to ensure we have all the server's warnings in memory.
    //    retrieveWarnings();
    //
    //    //Then we iterate through the ones that belongs to this server, looking for one which user
    //    //ID matches the one of the user.
    //    for (Warning warning : dynWarnings) {
    //        //Not so good looking but very clear
    //        if (warning.getUser() == member.getIdLong()) {
    //            return warning;
    //        }
    //    }
    //}

    ///**
    // * This method's purpose is to return the Warning's amount attribute value concerning the given
    // * member. To do so, it will run through the list of warnings of this server.
    // * 
    // * @param memberId The ID as a long of the member that we want to find the amount of warning of.
    // */
    //public int getMemberWarningAmount(long memberId) {
    //    //First step is to ensure we have all the server's warnings in memory.
    //    retrieveWarnings();
    //
    //    //Then we iterate through the ones that belongs to this server, looking for one which user
    //    //ID matches the one of the user.
    //    for (Warning warning : dynWarnings) {
    //        //Not so good looking but very clear
    //        if (warning.getUser() == memberId) {
    //            return warning;
    //        }
    //    }
    //}

    ///**
    // * This method's purpose is to return the Warning's amount attribute value concerning the given
    // * member. To do so, it will run through the list of warnings of this server.
    // * 
    // * @param member The member that we want to find the amount of warning of.
    // */
    //public int getMemberWarningAmount(Member member) {
    //    //First step is to ensure we have all the server's warnings in memory.
    //    retrieveWarnings();
    //
    //    //Then we iterate through the ones that belongs to this server, looking for one which user
    //    //ID matches the one of the user.
    //    for (Warning warning : dynWarnings) {
    //        //Not so good looking but very clear
    //        if (warning.getUser() == member.getIdLong()) {
    //            return warning;
    //        }
    //    }
    //}

    ///**
    // * This method will add a warning to the given member. It'll check that the member at the
    // * origin of the request is allowed to de so.
    // * If it is the case, then it will iterate through the server's warning list, to see whether
    // * the member already has one for him or if we need to create a new object.
    // * 
    // * @param originMember The member at the origin of the change. If it is the bot itself, then
    // *                     this member should be : this.JDAServer.getSelfMember().
    // * @param memberId The ID in a long shape of the member to warn.
    // * 
    // * @throws PermissionException When the member who is at the origin of the call doesn't have
    // *                             the adequate permissions.
    // */
    //public void warnMember(Member originMember, long memberId) throws PermissionException {
    //    if (!originMember.hasPermission(Permission.BAN_MEMBERS)) {
    //        throw new PermissionException(Main.english.memberBanMembersPermissionLack);
    //    }
    //
    //    Warning warning = findWarning(memberId);
    //
    //    if (warning == null) {
    //        warning = new Warning(this.ID, memberId); //!\ The constructor sets the amoung at 0!
    //    }
    //
    //    warning.incrementAmount();
    //}

    ///**
    // * This method will add a warning to the given member. It'll check that the member at the
    // * origin of the request is allowed to de so.
    // * If it is the case, then it will iterate through the server's warning list, to see whether
    // * the member already has one for him or if we need to create a new object.
    // * 
    // * @param originMember The member at the origin of the change. If it is the bot itself, then
    // *                     this member should be : this.JDAServer.getSelfMember().
    // * @param member The member to warn.
    // * 
    // * @throws PermissionException When the member who is at the origin of the call doesn't have
    // *                             the adequate permissions.
    // */
    //public void warnMember(Member originMember, Member member) throws PermissionException {
    //    if (!originMember.hasPermission(Permission.BAN_MEMBERS)) {
    //      throw new PermissionException(Main.english.memberBanMembersPermissionLack);
    //    }
    //
    //    Warning warning = findWarning(member.getIdLong());
    //
    //    if (warning == null) {
    //        warning = new Warning(this.ID, member.getIdLong()); //!\ The constructor sets the amoung at 0!
    //    }
    //
    //    warning.incrementAmount();
    //}

    ///**
    // * This method will remove a warning to the specified member. It'll check that the member at
    // * the origin if the request has adequate permissions.
    // * If it is the case, it will then look for the member's warning in the list, throw a minor
    // * RuntimeException if it isn't found, or decrease the amount attribute of the warning.
    // * 
    // * @param originMember The member at the origin of the change. If it is the bot itself, then
    // *                     this member should be : this.JDAServer.getSelfMember().
    // * @param memberId The ID in a long shape of the member to unwarn.
    // * 
    // * @throws PermissionException When the member who is at the origin of the call doesn't have
    // *                             the adequate permissions.
    // * @throws RuntimeException When the member specified has no warnings.
    // */
    //public void reduceMemberWarnings(Member originMember, long memberId) throws PermissionException, RuntimeException {
    //    if (!originMember.hasPermission(Permission.MODERATE_MEMBERS)) {
    //        throw new PermissionException(Main.english.memberModerateMembersPermissionLack);
    //    }
    //
    //    Warning warning = findWarning(memberId);
    //
    //    if (warning == null) {
    //        throw new RuntimeException("The specified user had no warning."); //Not an output message
    //    }
    //
    //    warning.decrementAmount();
    //}

    ///**
    // * This method will remove a warning to the specified member. It'll check that the member at
    // * the origin if the request has adequate permissions.
    // * If it is the case, it will then look for the member's warning in the list, throw a minor
    // * RuntimeException if it isn't found, or decrease the amount attribute of the warning.
    // * 
    // * @param originMember The member at the origin of the change. If it is the bot itself, then
    // *                     this member should be : this.JDAServer.getSelfMember().
    // * @param member The member to unwarn.
    // * 
    // * @throws PermissionException When the member who is at the origin of the call doesn't have
    // *                             the adequate permissions.
    // * @throws RuntimeException When the member specified has no warnings.
    // */
    //public void reduceMemberWarnings(Member originMember, Member member) throws PermissionException, RuntimeException {
    //    if (!originMember.hasPermission(Permission.MODERATE_MEMBERS)) {
    //        throw new PermissionException(Main.english.memberModerateMembersPermissionLack);
    //    }
    //
    //    Warning warning = findWarning(member.getIdLong());
    //
    //    if (warning == null) {
    //        throw new RuntimeException("The specified user had no warning."); //Not an output message
    //    }
    //
    //    warning.decrementAmount();
    //}

    /* UTILITARY METHODS */

    /**
     * A utilitary method that helps the treatment and clarity of role adding methods.
     * 
     * @param membersId The members to whom we should give the role
     * @param role The role to give to the members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions.
     */
    private void addRoleToMembers(Collection<Long> membersId, Role role) throws PermissionException {
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
            throw new PermissionException(Main.english.selfManageRolesPermissionLack);
        }

        for (long memberId : membersId) {
            this.JDAServer.addRoleToMember(this.JDAServer.getMemberById(memberId), role);
        }
    }

    /**
     * A utilitary method that helps the treatment and clarity of role exchanging methods.
     * 
     * @param membersId The members to whom we should exchange the roles
     * @param previousrole The role to remove from the members.
     * @param newRole The role to give to the members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions.
     */
    private void exchangeRoleOnMembers(Collection<Long> membersId, Role previousRole, Role newRole) throws PermissionException {
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
            throw new PermissionException(Main.english.selfManageRolesPermissionLack);
        }

        for (long memberId : membersId) {
            this.JDAServer.removeRoleFromMember(this.JDAServer.getMemberById(memberId), previousRole);
            this.JDAServer.addRoleToMember(this.JDAServer.getMemberById(memberId), newRole);
        }
    }

    /**
     * A utilitary method that helps the treatment and clarity of role removing methods.
     * 
     * @param membersId The members from whom we should remove the role
     * @param role The role to remove from the members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions.
     */
    private void removeRoleFromMembers(Collection<Long> membersId, Role role) throws PermissionException {
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
            throw new PermissionException(Main.english.selfManageRolesPermissionLack);
        }

        for (long memberId : membersId) {
            this.JDAServer.removeRoleFromMember(this.JDAServer.getMemberById(memberId), role);
        }
    }

    /**
     * This method makes sure every user respects the amount of warnings by banning the ones that
     * don't. It isn't particularly efficient, and because of that, it would be better not to call
     * it too often.
     * 
     * @throws PermissionException When the bot isn't allowed to ban members
     */
    private void checkWarningAmounts() throws PermissionException {
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.BAN_MEMBERS)) {
            throw new PermissionException(Main.english.selfBanMembersPermissonLack);
        }

        //1. Load all the Warnings of the server in the memory and in a local list
        //  -> Prerequisites : Warning class & an API request to retrieve all of them
        //2. For each of them, check the amount, to see if it is higher than allowed
        //3. Ban the members with too much warnings and add them to the banned list
    }

    /**
     * This method's purpose is to create a Warning object for every item of the warnings list.
     * Thanks to it, these will be stored in memory, and rapidly accessible for further actions.
     * 
     * @throws RuntimeException When there is a synchronization problem between the memory and the
     *                          dynamic list of Warning objects.
     */
    private void retrieveWarnings() {

        //1. Prepare the request to the API by creating the HTTP GET request specifying all the
        //   warings in the list.
        //   -> We'll need to check if we don't already have some in the memory. If we do, we'll
        //      need to send them at the top of the cyclic list before moving on to the next step.
        //if (this.warnings.size() < this.dynWarnings.size()) {
            //THIS CASE IS A MAJOR ERROR !! IT SHOULD NOT BE REACHED, as it means we have kept in
            //memory objects that SHOULD have been deleted !!

            //This case is particularly hard to treat because I can hardly know which item(s)
            //causes the problem.
            //To solve it, I will search for EVERY SINGLE object of this server's dynWarnings list
            //in the memory, and delete it if it isn't found in it. But this process is VERY
            //costful and has to be avoided at any cost!

            //for (Warning warning : dynWarnings) {
                //if (!Main.warningsIndexes.containsKey(warning.getID())) {
                    //this.dynWarnings.remove(warning);
                //}
            //}

            //throw new RuntimeException("MAJOR EXCEPTION : WARNING OBJECTS THAT SHOULD HAVE BEEN DESTROYED WERE KEPT IN-MEMORY!");
        //} else if (this.warnings.size() > this.dynWarnings.size()) {
            //We create a list that will contain the IDs of the Warnings to put in memory
            ArrayList<Long> warningsToRetrieve = new ArrayList<Long>();

            for (long warningID : warnings) {
                if (!Main.warningsIndexes.containsKey(warningID)) {
                    warningsToRetrieve.add(warningID);
                }
            }

            //2. Send the request and get the result as a x-tuple JSON array.
            //3. Parse the result and create all the instances of warning necessary.
            //4. Put all those instances in the memory list.
        //}
    }

    ///**
    // * This method aims to find the warning concerning the given member in the warning list.
    // * 
    // * @param memberId The member to whom we want to get the warning
    // * 
    // * @return The warning of this member, or null if it wasn't in the list.
    // */
    //@Nullable
    //private Warning findWarning(long memberId) {
    //    retrieveWarnings();
    //
    //    Warning warning;
    //
    //    for (Warning iterationWarning : dynWarnings) {
    //        if (iterationWarning.getUser() == memberId) {
    //            warning = iterationWarning;
    //
    //            return warning;
    //        }
    //    }
    //
    //    return warning;
    //}

    @Override
    public JsonObject getJson() {
        JsonObject jsonServer = new JsonObject();

        //To do!

        return jsonServer;
    }

    @Override
    public long getID() {
        return this.ID;
    }
    
}
