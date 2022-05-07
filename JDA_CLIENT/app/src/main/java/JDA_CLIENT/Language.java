package JDA_CLIENT;

import java.io.FileNotFoundException;

/**
 * This class will contain all the string messages for the given language. For now they are going
 * to be defined here, but the goal is to let the parseStrings method, called at the startoff, fill
 * these all by itself out of the lang.lang file in the resources directory.
 * 
 * @author RedNeath
 */
public class Language {
    private String lang;

    /**
     * These are the strings that will be initialized later on by the parseStrings() method.
     */
    public String commandNameOrOutputTooShort = "Command name or output too short!";

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
}
