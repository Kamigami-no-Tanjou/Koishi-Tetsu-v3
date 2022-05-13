package JDA_CLIENT.COMMANDS;

import JDA_CLIENT.API_RESOURCES.Command;

/**
 * This class is a subclass of Command. It represents the commands that will be provided by the bot
 * in any server it is on.
 * It is essentially there to separate CustomCommands to DefaultCommands. For instance, thanks to
 * this class, all the DefaultCommands can be added to a list, in which we can't include any custom
 * command.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public abstract class DefaultCommand extends Command {}
