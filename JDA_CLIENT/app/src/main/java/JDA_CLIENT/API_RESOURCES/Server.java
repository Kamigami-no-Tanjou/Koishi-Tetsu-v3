package JDA_CLIENT.API_RESOURCES;

import org.json.simple.JsonObject;

import JDA_CLIENT.Main;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.Permission;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.entities.User;
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
        this.mutedCooldown = 2;
        this.maxWarn = 3;
        this.cooldown = 150;
        this.banned = new ArrayList<Long>();
        this.warnings = new ArrayList<Long>();
        this.prefix = "kt";
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
        this.mutedUsers = new ArrayList<Long>();
        this.mutedUsers.addAll(mutedUsersCollection);
        this.banned = new ArrayList<Long>();
        this.banned.addAll(bannedCollection);
        this.warnings = new ArrayList<Long>();
        this.warnings.addAll(warningsCollection);
        //This one is treated a bit differently as we have to retrieve all the objects form their ID.
        this.autoRoles = new ArrayList<Role>();
        for (Long l : autoRolesCollection) {
            this.autoRoles.add(this.JDAServer.getRoleById(l));
        }
        this.reactionRoles = new ArrayList<Long>();
        this.reactionRoles.addAll(reactionRolesCollection);
        this.customCommands = new ArrayList<Long>();
        this.customCommands.addAll(customCommandsCollection);
    }

    /**
     * This method will have to be called by the MuteUser command after parsing the sender's
     * mesage. It will basically execute the actions to make the sentence effective.
     * 
     * @param member The member to mute. Won't accept it as an Id (long).
     * @param time The amount of hours the user will be muted on the server. If the sender didn't
     *             specify anything for it, the value 0 will have to be passed, which will make the
     *             method use the server's default value.
     * 
     * @throws PermissionException When the bot can't perform the action because he doesn't have
     *                             the permissions for it.
     * 
     * @return The amount of time, as a long, for which the specified user's been muted. Useful for
     *         the success output message.
     */
    public long muteUser(Member member, long time) throws PermissionException {
        //First we have to give the user the muted role if it exists
        Role mutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

        //This works because if the role we look for can't be found, the getRoleById method reurns
        //a null Role.
        if (mutedRole != null) {
            if (this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
                this.JDAServer.addRoleToMember(member, mutedRole);
            } else {
                throw new PermissionException(Main.english.manageRolesPermissionLack);
            }
        }

        //Note that the muted role can intentionally not be set, and on top of that, that role can
        //be just a label, so we have to timeout the user using discord functions.
        //In order to do that, we simply check the bot's permissions and throw a PermissionException
        //if it doesn't have the required permissions.
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.moderateMembersPermissionLack);
        }

        //This could be in a else statement, but as the throw Exception makes the method return, it
        //isn't mandatory.
        if (time <= 0 || time > 672) { //If the provided cooldown is wrong, default value is used.
            member.timeoutFor(this.mutedCooldown, TimeUnit.HOURS);
            //Then we add the user to the muted list.
            this.mutedUsers.add(member.getIdLong());

            //And we return the mutedCooldown to tell the calling method how long the user has been
            //muted for.
            return this.mutedCooldown;
        } else {
            member.timeoutFor(time, TimeUnit.HOURS);
            //Same here, but we return time instead.
            this.mutedUsers.add(member.getIdLong());
            return time;
        }
    }

    /**
     * This method will have to be called by the UnmuteUser command after parsing the sender's
     * mesage. It will basically execute the actions to revoque the sentence.
     * 
     * @param member The member to unmute. Won't accept it as an Id (long).
     * 
     * @throws PermissionException When the bot can't perform the action because he doesn't have
     *                             the permissions for it.
     */
    public void unmuteUser(Member member) throws PermissionException {
        //Just like the muteUser method, we're gonna check if there is a role attributed to muted
        //users. If so, we will need to make sure the bot has the right permissions to edit the
        //user's role, and then remove that role.

        Role mutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

        //Again, this works because if the role we look for can't be found, the getRoleById method
        //returns a null role.
        if (mutedRole != null) {
            if (this.JDAServer.getSelfMember().hasPermission(Permission.MANAGE_ROLES)) {
                this.JDAServer.removeRoleFromMember(member, mutedRole);
            } else {
                throw new PermissionException(Main.english.manageRolesPermissionLack);
            }
        }

        //Now that the role is removed if there was one, we need to revoque the user's timeout.
        //Let's check permissions once again and then act if possible :
        if (!this.JDAServer.getSelfMember().hasPermission(Permission.MODERATE_MEMBERS)) {
            throw new PermissionException(Main.english.moderateMembersPermissionLack);
        }

        //Finally, we remove the user's timeout.
        member.removeTimeout();
        //And we remove the user from the muted list.
        this.mutedUsers.remove(member.getIdLong());
    }

    /**
     * This method aims to change the muted role of the server. Note that this method can also be
     * used for removing the muted role. For that you simply have to give it a value that doesn't
     * correspond to any role in the concerned server.
     * 
     * @param mutedRoleId The id of the new role for muted members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions. Could be caught
     *                             but I prefer to let it get up to the call of this method to make
     *                             sure the output is send to the user.
     */
    public void setMutedRole(long mutedRoleId) throws PermissionException {
        //This might actually sound werid because the muted role is stored via its id, but this
        //method will simply call its overload with a Role as a parameter, as we have to verify
        //whether the id given corresponds to any existing role or not.

        //Reasons behind that are that we want the muted users to change roles if the role is
        //modified and to remove the role from them if it is changed to an invalid one. Please see
        //the setMutedRole(Role mutedRole) method for a more accurate explanation of this.
        Role mutedRole = JDAServer.getRoleById(mutedRoleId);
        setMutedRole(mutedRole);
    }

    /**
     * This method aims to change the muted role of the server. Note that this method can also be
     * used for removing the muted role. For that you simply have to give it a null Role.
     * 
     * @param mutedRole The new role for muted members.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions. Could be caught
     *                             but I prefer to let it get up to the call of this method to make
     *                             sure the output is send to the user.
     */
    public void setMutedRole(Role mutedRole) throws PermissionException {
        //Here we have two possibilities :
        //1 : The Role given is null and we need to remove the muted role from the muted users
        //2 : The Role given is existing, which means we have to change it for all muted users
        
        if (mutedRole != null) {
            //Case 2 :

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
            removeMutedRole();
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

    @Nullable
    /**
     * This method returns the role associated to mutedUsers. Notice that it will return a null
     * value if there is no role associated, or if it is incorrect (if it has been deleted for
     * instance).
     * 
     * @return The role associated to mutedUsers.
     */
    public Role getMutedRole() {
        return this.JDAServer.getRoleById(this.mutedRoleId);
    }

    /**
     * This method aims to remove the muted role of the server. It works by simply putting it at 0
     * and removing previous roles (if there was one) from the mutedMembers.
     * 
     * @throws PermissionException When the bot doesn't have the right permissions. Could be caught
     *                             but I prefer to let it get up to the call of this method to make
     *                             sure the output is send to the user.
     */
    public void removeMutedRole() throws PermissionException {
        //We retrieve the role previously applied.
        Role previousMutedRole = this.JDAServer.getRoleById(this.mutedRoleId);

        if (previousMutedRole != null) {
            removeRoleFromMembers(this.mutedUsers, previousMutedRole);
        }

        //In the end, we give a 0 value to the mutedRole.
        this.mutedRoleId = 0;
    }

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
            throw new PermissionException(Main.english.manageRolesPermissionLack);
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
            throw new PermissionException(Main.english.manageRolesPermissionLack);
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
            throw new PermissionException(Main.english.manageRolesPermissionLack);
        }

        for (long memberId : membersId) {
            this.JDAServer.removeRoleFromMember(this.JDAServer.getMemberById(memberId), role);
        }
    }

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
