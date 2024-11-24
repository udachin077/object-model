from object_model import ObservableList, NotifyListChangedEventArgs

collection = ObservableList[str]("abcdefghijklm")


@collection.collection_changed.add
def collection_changed(sender, e: NotifyListChangedEventArgs):
    print(f"Action: {e.action}")


def collection_changed_1(sender, e: NotifyListChangedEventArgs):
    print(f"Sender: {sender}")


collection.remove("a")
# Action: NotifyCollectionChangedAction.REMOVE
collection.collection_changed += collection_changed_1
collection.append("a")
# Action: NotifyCollectionChangedAction.ADD
# Sender: ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'a']
