package JDA_CLIENT.API_RESOURCES;

import org.json.simple.JsonObject;

/**
 * This interface helps making sure that classes which are meant to be exported to the API have the
 * necessary methods for that.
 * 
 * @author RedNeath
 * Copyright © 2022 Kamigami no Tanjou
 */
public interface ApiResource {
    /**
     * This method returns the object under a Json shape. This will be used for posting new objects
     * in the API.
     * 
     * @return The Json shaped object.
     */
    public abstract JsonObject getJson();

    /**
     * This method returns the ID of the object in the API.
     * 
     * @return An integer greater than 0.
     */
    public abstract long getID();
}
