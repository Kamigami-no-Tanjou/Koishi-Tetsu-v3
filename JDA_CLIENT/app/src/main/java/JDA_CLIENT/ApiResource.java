package JDA_CLIENT;

import com.github.cliftonlabs.json_simple.JsonObject;

/**
 * This interface helps making sure that classes which are meant to be exported to the API have the
 * necessary methods for that.
 * 
 * @author RedNeath
 */
public interface ApiResource {
    /**
     * This method returns the object under a Json shape. This will be used for posting new objects
     * in the API.
     * 
     * @return The Json shaped object.
     */
    public abstract JsonObject getJson();
}
