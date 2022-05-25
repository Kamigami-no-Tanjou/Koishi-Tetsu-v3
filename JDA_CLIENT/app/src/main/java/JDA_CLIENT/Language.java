package JDA_CLIENT;

import java.io.FileNotFoundException;

import JDA_CLIENT.EXCEPTIONS.ParseException;

/**
 * This class will contain all the string messages for the given language. For now they are going
 * to be defined here, but the goal is to let the parseStrings method, called at the startoff, fill
 * these all by itself out of the lang.lang file in the resources directory.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class Language {
    private String lang;

    /**
     * These are the strings that will be initialized later on by the parseStrings() method.
     */
    public String commandNameOrOutputTooShort       = "The command name, or its output is too short! It's like you're telling me to eat the stone you have in your hand, while your hand is empty! :cry:";
    public String commandDisabledTriggered          = "I can't do something you told me not to! :persevere: use the following command to enable the command:";
    public String manageRolesPermissionLack         = "Wait, roles? What are roles? That wasn't what I signed for! :confounded: I need your permission to manage them...";
    public String memberManageRolesPermissionLack   = "I'm sorry, but I'm not too sure you were allowed to manage roles :eyes:";
    public String moderateMembersPermissionLack     = "Mmmh... Sure, but... I'd need you to allow me to moderate members :point_right::point_left:";
    public String memberManageServerPermissionLack  = "Stop right there! I can't let you do that, you need the permission to manage the server for that.";
    public String mutedCooldownTooHigh              = "That long?! Best I can do is 672 hours...";
    public String mutedCooldownTooLow               = "Hum, what? I... can't go against the time, I guess? Minimum value is 1 hour.";

    /**
     * This constructor will build a language and initialize its values by calling the parseStrings
     * method.
     * 
     * @param lang The two chars length name of the language to create.
     * 
     * @throws Exception Can whether be a FileNotFoundException or a ParseException. The two of
     * those will cause the constructor to stop and the program to stop.
     */
    public Language(String lang) throws Exception {
        this.lang = lang;

        parseStrings();
    }

    /**
     * This method will parse the lang.lang file and put the right messages in the right attribute.
     * 
     * @throws FileNotFoundException When the file isn't found (meaning the language is either
     * incorrect or not yet part of the translations)
     * @throws ParseException When the parser couldn't read the file properly (meaning there is an
     * error in the file that was being parsed).
     */
    public void parseStrings() throws FileNotFoundException, ParseException {
        //Will parse the lang.lang file and put the right messages in the right attribute.
    }

    /**
     * A simple getter that allows us to know what the language is.
     * 
     * @return The two letters long name of the language. (ex. EN for English, SV for Swedish...)
     */
    public String getLang() {
        return this.lang;
    }
}
