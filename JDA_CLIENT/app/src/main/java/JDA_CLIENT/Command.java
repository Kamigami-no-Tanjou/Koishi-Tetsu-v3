package JDA_CLIENT;

import java.util.concurrent.ExecutionException;

import net.dv8tion.jda.api.events.Event;

/**
 * This abstract class represents a command. It is meant to be implemented by all the default and
 * customized commands, providing them a few essential methods and attributes.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public abstract class Command {
    /** The name of the command (what comes after the prefix). */
    private String name;
    /** Whether the command is enabled or not. If it's not, the command won't be executed. */
    private boolean enabled;

    //Inheriting classes may have other attributes of other types here.
    
    /**
     * This method is the one that will starts the execution of the command.
     * It will recieve the args of the command, which will then be parsed and inserted into the
     * commands attributes via the method parseArgs().
     * After that, the command will proceed.
     * 
     * @param event The event to which this command is attached. Will help a lot for processing.
     * @param commandArgs The args of the command. Basically what comes after the name.
     * 
     * @throws IllegalArgumentException When one or more arguments are absent or incorrect.
     * @throws ExecutionException When the processing can't succeed.
     */
    public void Treatment(Event event, String commandArgs) throws IllegalArgumentException, ExecutionException {
        try {
            //We try to parse the arguments.
            parseArgs(commandArgs);

            //Then we try to process the command.
            processCommand(event);

        } catch (TreatmentException exception) {
            //And if it fails, we look at what exception was raised and throw the right type of exception.
            if (exception.getType().equals("ParseException")) {
                throw new IllegalArgumentException(exception.getMessage(), exception.getCause());
            } else {
                throw new ExecutionException(exception.getMessage(), exception.getCause());
            }
        }
    }

    /**
     * This method will be called by the Treatment method in order to put the args of the command
     * in the correct attributes.
     * 
     * @param args The args of the command.
     * 
     * @throws ParseException When one argument is absent or incorrect.
     */
    protected abstract void parseArgs(String args) throws ParseException;

    /**
     * This method will be called by the Treatment method in order to process the command.
     * 
     * @param event The event to which this command is attached.
     * 
     * @throws ProcessException When one operation failed.
     */
    protected abstract void processCommand(Event event) throws ProcessException;

    //Inheriting classes may have several extra methods to handle their task.
}
