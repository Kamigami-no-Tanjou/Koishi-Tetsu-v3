package JDA_CLIENT;

import java.util.HashMap;

import JDA_CLIENT.COMMANDS.CustomCommand;

/**
 * This class is the heart of the bot.
 * It contains all the memory arrays (which are static since it can't be instanciated), starts off
 * the bot, defines the dictionnary of commands, reads texts files and provides a few core methods.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class Main {
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
    }
}
