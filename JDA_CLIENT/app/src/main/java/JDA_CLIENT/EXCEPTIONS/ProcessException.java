package JDA_CLIENT.EXCEPTIONS;

/**
 * This class is the Exception class for the command's processing.
 * It is raised whenever the processing of a command fails.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public class ProcessException extends TreatmentException {

    @Override
    public String getType() {
        return "ProcessException";
    }
}