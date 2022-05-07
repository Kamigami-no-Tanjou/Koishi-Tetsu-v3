package JDA_CLIENT;

/**
 * This class is the Exception class for the command's processing.
 * It is raised whenever the processing of a command fails.
 * 
 * @author RedNeath
 */
public class ProcessException extends TreatmentException {

    @Override
    public String getType() {
        return "ProcessException";
    }
}