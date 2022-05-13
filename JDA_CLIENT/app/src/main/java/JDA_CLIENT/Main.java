package JDA_CLIENT;

import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;

import javax.security.auth.login.LoginException;

import JDA_CLIENT.COMMANDS.*;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.requests.GatewayIntent;

/**
 * This class is the heart of the bot.
 * It contains all the memory arrays (which are static since it can't be instanciated), starts off
 * the bot, defines the dictionnary of commands, reads texts files and provides a few core methods.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class Main extends ListenerAdapter {
    /** These constants defines the amount of places in the memory for all object types. */
    public static final int MAX_SERVERS_IN_MEMORY = 50;
    public static final int MAX_USERS_IN_MEMORY = 50 * MAX_SERVERS_IN_MEMORY;
    public static final int MAX_REACROLES_IN_MEMORY = 10 * MAX_SERVERS_IN_MEMORY;
    public static final int MAX_CUSTOM_COMMANDS_IN_MEMORY = 10 * MAX_SERVERS_IN_MEMORY;
    public static final int MAX_CHARACTERS_IN_MEMORY = 50 * MAX_SERVERS_IN_MEMORY;
    public static final int MAX_STATS_IN_MEMORY = 6 * MAX_CHARACTERS_IN_MEMORY * MAX_SERVERS_IN_MEMORY;
    public static final int MAX_WARNINGS_IN_MEMORY = 50 * MAX_SERVERS_IN_MEMORY;
    //Note that they all depends on the amount of servers defined.

    /**
     * These are the arrays of objects. Theye are cyclic and sorted by date of use. The indexes of
     * their elements are referenced in HashMaps for better efficiency.
     */
    //private static Server[] servers = new Server[MAX_SERVERS_IN_MEMORY];
    //private static User[] users = new User[MAX_USERS_IN_MEMORY];
    //private static ReactionRole[] reactionRoles = new ReactionRoles[MAX_REACROLES_IN_MEMORY];
    private static CustomCommand[] customCommands = new CustomCommand[MAX_CUSTOM_COMMANDS_IN_MEMORY];
    //private static Chara[] characters = new Chara[MAX_CHARACTERS_IN_MEMORY];
    //private static Stat[] stats = new Stat[MAX_STATS_IN_MEMORY];
    //private static Warning[] warnings = new Warning[MAX_WARNINGS_IN_MEMORY];

    private static float loadFactor = (float) 0.8;

    /**
     * These are the HashMaps discussed earlier. They associate the ID of each element (as the key)
     * with their index (as the value) in their respectiv array. As a result, these are all
     * Integer/Integer HashMaps.
     */
    private static HashMap<Integer, Integer> serverIndexes      = new HashMap<Integer, Integer>(8, loadFactor);
    private static HashMap<Integer, Integer> userIndexes        = new HashMap<Integer, Integer>(196, loadFactor);
    private static HashMap<Integer, Integer> reacRolesIndexes   = new HashMap<Integer, Integer>(40, loadFactor);
    private static HashMap<Integer, Integer> commandsIndexes    = new HashMap<Integer, Integer>(40, loadFactor);
    private static HashMap<Integer, Integer> characterIndexes   = new HashMap<Integer, Integer>(196, loadFactor);
    private static HashMap<Integer, Integer> statsIndexes       = new HashMap<Integer, Integer>(586, loadFactor);
    private static HashMap<Integer, Integer> warningsIndexes    = new HashMap<Integer, Integer>(196, loadFactor);
    //The initial size will have to be recalculated if the amount of servers in memory increases!!!

    /**
     * We add to that another HashMap that will contain the whole list of commands, referrenced by
     * name.
     * As the amount of default commands will remain the same, we simply initialize it with a
     * capacity matching the amount and with a loadFactor of 1, so that it stays as optimized as it
     * can be.
     * CHECK THIS WHEN YOU ADD A COMMAND!!!
     */
    private static HashMap<String, DefaultCommand> defaultCommands = new HashMap<String, DefaultCommand>(0, 1);

    /**
     * Here we define all the languages available.
     */
    public static Language english;

    public static void main(String[] args) {
        try {
            //We try to get all the languages to initialize themselves...
            english = new Language("EN");
        } catch (Exception e) {
            //... and we catch the exception if there is one.
            
            //At this point, the program will shut down and write the exception it recieved in the
            //log file. But this is yet to be developped.
        }

        
        try {
            //We build our JDA instance with the bot token (args[0]).
            JDABuilder jda = JDABuilder.createDefault(args[0]);
            
            //We add the event listeners
            jda.addEventListeners(new Main());

            //Then we initialize the intents
            Collection<GatewayIntent> intents = new HashSet<>();
            intents.add(GatewayIntent.GUILD_MESSAGES);
            intents.add(GatewayIntent.DIRECT_MESSAGES);
            intents.add(GatewayIntent.GUILD_VOICE_STATES);
            intents.add(GatewayIntent.GUILD_EMOJIS);
            //intents.add(GatewayIntent.GUILD_BANS); Not necessary yet
            //intents.add(GatewayIntent.GUILD_MEMBERS); Not necessary yet
            //intents.add(GatewayIntent.GUILD_MESSAGE_REACTIONS); Not sure it will be necessary
            //intents.add(GatewayIntent.GUILD_PRESENCES); Not sure it will be necessary

            //We add the intents
            jda.setEnabledIntents(intents);

            //We add the bot activity
            jda.setActivity(Activity.watching("a stone he'd like to eat"));

            //And we finally build the bot
            jda.build();
            
        } catch (LoginException e) {
            
            e.printStackTrace();
        }
    }
}
