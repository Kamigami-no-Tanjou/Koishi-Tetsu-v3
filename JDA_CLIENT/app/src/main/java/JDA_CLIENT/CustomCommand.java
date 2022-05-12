package JDA_CLIENT;

import com.github.cliftonlabs.json_simple.JsonObject;

import net.dv8tion.jda.api.events.Event;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;

/**
 * This class is a subclass of Command. It represents the commands made by users for themselves.
 * For now it only takes one name, one output and returns the output when triggered.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public abstract class CustomCommand extends Command implements ApiResource {
    /** The output for this custom command */
    private String output;

    /**
     * This constructor creates one iteration of a CustomCommand. In order to do so, it'll need the
     * command's name and the command's output.
     * 
     * @param name The name of the command i.e. what will come after the prefix.
     * @param output What the bot will send back to the server when the command will be triggered
     * 
     * @throws IllegalArgumentException When the name or output are too short. (< 1)
     */
    public CustomCommand(String name, String output) throws IllegalArgumentException {
        if (name.length() < 1 || output.length() < 1) {
            throw new IllegalArgumentException(Main.english.commandNameOrOutputTooShort); //Will have to be changed for the server's language
        }
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
    protected void processCommand(Event event) throws ProcessException {
        //This works if we assume that custom commands can only be triggered via a message.
        MessageReceivedEvent castedEvent = (MessageReceivedEvent) event;

        castedEvent.getChannel().sendMessage(output).queue();
    }
    
    @Override
    public JsonObject getJson() {
        JsonObject jsonCustomCommand = new JsonObject();

        return jsonCustomCommand;
    }
}
