from abc import ABC, abstractmethod

# Abstract base class for all observers
class Observer(ABC):
    @abstractmethod
    def update(self, event_name, payload):
        pass

# Logs stock save events
class StockSavedObserver(Observer):
    def update(self, event_name, payload):
        if event_name == "stock_saved":
            ticker = payload.get('ticker')
            key = payload.get('key')
            print(f"Stock: {ticker} saved to portfolio!")

# Logs favorite add/remove events
class FavoriteChangedObserver(Observer):
    def update(self, event_name, payload):
        if event_name == "favorite_added":
            ticker = payload.get('ticker')
            print(f"[Favorites] {ticker} was added successfully to favorites!")
        elif event_name == "favorite_removed":
            ticker = payload.get('ticker')
            print(f"[Favorites] {ticker} was deleted successfully from favorites!")

# Manages observers and notifies them of events.
class Notifier:
    def __init__(self):
        self._observers = []

    # Subscribe an observer to receive event notifications
    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    # Unsubscribe an observer from event notifications
    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    # Notify all observers
    def notify(self, event_name, payload):
        for observer in self._observers:
            try:
                observer.update(event_name, payload)
            except Exception as e:
                print(f"Notifier error: {e}")


# Global notifier instance
notifier = Notifier()

# Register default observers
notifier.subscribe(StockSavedObserver())
notifier.subscribe(FavoriteChangedObserver())
