package JDA_CLIENT;

/**
 * This class is the general Exception class for the Command's treatment. It has two sub-classes :
 * ParseException and ProcessException, which will respectively be called by the methods parseArgs
 * and processCommand.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public abstract class TreatmentException extends Exception {
    /**
     * This method helps knowing what is the source of the exception.
     * 
     * @return The exact name of the Exception.
     */
    public abstract String getType();  
}
