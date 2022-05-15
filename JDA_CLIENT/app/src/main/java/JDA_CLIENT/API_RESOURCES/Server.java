package JDA_CLIENT.API_RESOURCES;

import org.json.simple.JsonObject;

import JDA_CLIENT.COMMANDS.CustomCommand;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Role;

import java.util.ArrayList;
import java.util.Collection;

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
    //private ArrayList<Long> mutedUsers;
    /** This is the role to give to muted users. Can be null. */
    private Role mutedRole;
    /** This is the amount of warn needed before the user gets banned. */
    private int maxWarn;
    /** This is the cooldown time in days before a warned user loses one warn. */
    private int cooldown;
    /** This is the list of users banned from the server. Can be empty. */
    //private ArrayList<Long> banned;
    /** This is the list of warnings linked to this server. Can be empty. */
    //private ArrayList<Long> warnings;
    /** This is the prefix used to recognized a custom command. */
    private String prefix;
    /** This is the list of roles to give to a user joining the server. Can be empty. */
    private ArrayList<Role> autoRoles;
    /** This is the list of reaction roles linked to this server. Can be empty. */
    //private ArrayList<Long> reactionRoles;
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
        //this.mutedUsers = new ArrayList<Long>();
        this.maxWarn = 3;
        this.cooldown = 150;
        //this.banned = new ArrayList<Long>();
        //this.warnings = new ArrayList<Long>();
        this.prefix = "kt";
        this.autoRoles = new ArrayList<Role>();
        //this.reactionRoles = new ArrayList<Long>();
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
        this.mutedRole = this.JDAServer.getRoleById(server.getLong("mutedRole")); //ugly....
        this.maxWarn = server.getInteger("maxWarn");
        this.cooldown = server.getInteger("cooldown");
        this.prefix = server.getString("prefix");

        //And finally we initialize the arrays and add the content of the mathcing collection.
        //this.mutedUsers = new ArrayList<Long>();
        //this.mutedUsers.addAll(mutedUsersCollection);
        //this.banned = new ArrayList<Long>();
        //this.banned.addAll(bannedCollection);
        //this.warnings = new ArrayList<Long>();
        //this.warnings.addAll(warningsCollection);
        //This one is treated a bit differently as we have to retrieve all the objects form their ID.
        this.autoRoles = new ArrayList<Role>();
        for (Long l : autoRolesCollection) {
            this.autoRoles.add(this.JDAServer.getRoleById(l));
        }
        //this.reactionRoles = new ArrayList<Long>();
        //this.reactionRoles.addAll(reactionRolesCollection);
        this.customCommands = new ArrayList<Long>();
        this.customCommands.addAll(customCommandsCollection);
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
