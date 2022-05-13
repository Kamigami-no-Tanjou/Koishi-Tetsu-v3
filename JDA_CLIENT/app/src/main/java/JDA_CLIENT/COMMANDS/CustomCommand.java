package JDA_CLIENT.COMMANDS;

import com.github.cliftonlabs.json_simple.JsonObject;

import JDA_CLIENT.Main;
import JDA_CLIENT.API_RESOURCES.ApiResource;
import JDA_CLIENT.API_RESOURCES.Command;
import JDA_CLIENT.EXCEPTIONS.ParseException;
import JDA_CLIENT.EXCEPTIONS.ProcessException;
import net.dv8tion.jda.api.events.Event;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;

/**
 * This class is a subclass of Command. It represents the commands made by users for themselves.
 * For now it only takes one name, one output and returns the output when triggered.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class CustomCommand extends Command implements ApiResource {
    /**
     * This constant variable gives the index for the custom command in the ApiResource array that
     * is used for processing a command.
     */
    public static final int INDEX = 2;
    /** This represents the ID assigned to this command in the API. */
    private int ID;
    /** The output for this custom command */
    private String output;
    /** Whether the command is enabled or not. If it's not, the command won't be executed. */
    private boolean enabled;
    private int cooldown;

    /**
     * This constructor creates one iteration of a CustomCommand. In order to do so, it'll need the
     * command's name and the command's output.
     * 
     * @param name The name of the command i.e. what will come after the prefix.
     * @param output What the bot will send back to the server when the command will be triggered
     * 
     * @throws IllegalArgumentException When the name or output are too short. (< 1)
     */
    public CustomCommand(int ID, String name, String output) throws IllegalArgumentException {
        if (name.length() < 1 || output.length() < 1) {
            throw new IllegalArgumentException(Main.english.commandNameOrOutputTooShort); //Will have to be changed for the server's language
        /*} else if (ID < 0) {
            throw new InvalidIdentifierException();
        */
        } else {
            this.name = name;
            this.output = output;
            this.cooldown = 0;
            this.ID = ID;
        }
    }

    /**
     * This method enables the command if it was disabled, or doesn't do anything.
     */
    public void enable() {
        this.enabled = true;
    }

    /**
     * This method disables the command if it was enabled, or doesn't do anything.
     */
    public void disable() {
        this.enabled = false;
    }
    
    @Override
    protected void parseArgs(String args) throws ParseException {
        /* We will parse the args as if we were in a terminal.
         * That is to say, they will be splitted by a ' ', except if the split character is within
         * a "" statement.
         */
        
         //In this case we won't do anything as we don't allow args for the custom commands yet
    }

    @Override
    protected void processCommand(ApiResource[] sources, Event event) throws ProcessException {
        //This works if we assume that custom commands can only be triggered via a message.
        MessageReceivedEvent castedEvent = (MessageReceivedEvent) event;

        //We first check that the command is enabled
        if (enabled) {
            //And if it is, we send the output in the channel where the command has been triggered.
            castedEvent.getChannel().sendMessage(output).queue();
        } else if (cooldown == 0) {
            //If the command has been triggered but is disabled, and the cooldown has reached 0, we
            //send him the instructions to enable the command back.
            StringBuilder help = new StringBuilder(Main.english.commandDisabledTriggered); //Will have to be changed for the server's language
            /*help.append(sources[Server.INDEX].getPrefix());
            help.append(EnableCommand.getName());*/
            help.append(" ");
            help.append(this.ID);

            castedEvent.getChannel().sendMessage(help.toString()).queue();

            cooldown = 3;
        } else {
            //Otherwise we reduce the cooldown, so that when the user really want the command to
            //execute, he'll get the help message faster.
            cooldown--;
        }
    }
    
    @Override
    public JsonObject getJson() {
        JsonObject jsonCustomCommand = new JsonObject();

        //To do!

        return jsonCustomCommand;
    }

    @Override
    public int getID() {
        return this.ID;
    }
}
