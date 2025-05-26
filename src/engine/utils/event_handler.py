class EventHandler:
    """
    A central event manager to dispatch events to registered listeners.
    This decouples event handling logic from the main game loop and individual components.
    """
    def __init__(self):
        # A dictionary to store listeners.
        # Keys are event types (e.g., pygame.QUIT, pygame.KEYDOWN, or custom strings).
        # Values are lists of callable functions/methods.
        self._listeners = {}

    def register_listener(self, event_type, callback):
        """
        Registers a callback function/method to be called when a specific event_type occurs.

        Args:
            event_type: The type of event to listen for (e.g., pygame.QUIT, "GAME_START").
            callback: The function or method to call when the event is posted.
                      It should accept one argument: the event object.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)
        # print(f"Registered listener for {event_type}: {callback.__name__}") # For debugging

    def unregister_listener(self, event_type, callback):
        """
        Unregisters a callback function/method. Useful for cleanup when objects are destroyed
        or states change.

        Args:
            event_type: The type of event the callback was listening for.
            callback: The function or method to remove.
        """
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            if not self._listeners[event_type]: # Remove key if no listeners left
                del self._listeners[event_type]
            # print(f"Unregistered listener for {event_type}: {callback.__name__}") # For debugging


    def post(self, event):
        """
        Dispatches an event to all registered listeners for that event's type.

        Args:
            event: The event object to be dispatched. This can be a pygame.event.Event
                   or a custom event object/dictionary.
        """
        # For Pygame events, event.type is an integer.
        # For custom events, you might use a string attribute, e.g., event.get('type')
        event_type = getattr(event, 'type', None) # Try to get 'type' attribute
        if event_type is None and isinstance(event, dict) and 'type' in event:
            event_type = event['type'] # If it's a dict, check for 'type' key

        if event_type in self._listeners:
            # Iterate over a copy of the list to prevent issues if listeners unregister themselves
            # during the iteration (e.g., a one-shot listener).
            for listener in list(self._listeners[event_type]):
                try:
                    listener(event)
                except Exception as e:
                    print(f"Error dispatching event {event_type} to {listener.__name__}: {e}")

    def clear_listeners(self, event_type=None):
        """
        Clears all listeners for a specific event type, or all listeners for all types
        if event_type is None.
        """
        if event_type:
            if event_type in self._listeners:
                del self._listeners[event_type]
        else:
            self._listeners.clear()

# You can also define custom event types as constants here or in a separate file
# For example:
# CUSTOM_EVENT_GAME_START = pygame.USEREVENT + 1
# CUSTOM_EVENT_PLAYER_DIED = pygame.USEREVENT + 2