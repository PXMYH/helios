class ItemsProvider():
    def __init__(self, items):
        self._items = items

    def get(self, number_of_items):
        if not self._items:
            return []
        
        if number_of_items > len(self._items):
            number_of_items = len(self._items)
            
        return self._items[0, number_of_items]
