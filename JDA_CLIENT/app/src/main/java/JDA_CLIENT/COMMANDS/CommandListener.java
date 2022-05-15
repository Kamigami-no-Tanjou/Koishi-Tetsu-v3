package JDA_CLIENT.COMMANDS;

import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

/**
 * This class listens for events linked to commands. Its role is to start the right treatment when
 * a command is called by the user.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class CommandListener extends ListenerAdapter {

    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {
        //In this case, we know it is a default command that has been triggered.
        //We are simply going to take a look at the name to determine which one it is.
        String commandName = event.getName();

        switch (commandName) {
            //Test command
            case "test":
                event.getChannel().sendMessageFormat("Test!").queue();
                break;
        
            //Ping command
            case "ping":
                event.getChannel().sendMessage("Pong!");
                break;
        }
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        //In this case, it can be a custom command or nothing at all.
        //We'll go through all our list of custom commands for the given server, and then we'll
        //credit the user some exp for the message sent.
    }
}
