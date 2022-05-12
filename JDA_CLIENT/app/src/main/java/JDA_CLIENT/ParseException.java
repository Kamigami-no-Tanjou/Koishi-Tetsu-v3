package JDA_CLIENT;

/**
 * This class is the Exception class for the command's args parsing.
 * It is raised whenever the parsing of a command's args fails.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class ParseException extends TreatmentException {

    @Override
    public String getType() {
        return "ParseException";
    }
}
