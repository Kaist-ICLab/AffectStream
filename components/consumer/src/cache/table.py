"""
Cache implementation replacing Faust's RocksDB table().
Uses dbm(https://docs.python.org/3/library/dbm.html).
"""
from contextlib import contextmanager
import dbm.gnu
import os
import pickle


class Cache:
    """
    Wrapper class for dbm.
    Supports implicit serializaion/deserialization.
    """
    def __init__(self, filename: str = "cache.dbm"):
        """
        :param filename: filename of the dbm database. created if not exists.
        """
        dbm_path = os.path.abspath(os.path.join(__file__, "..", filename))
        self.db = dbm.gnu.open(dbm_path, "c")

    def get(self, key: str) -> any:
        """
        Returns the cache indexed by key.

        **WARNING: Unlike dictionary, the cache itself does not change even if the returned value is modified,
        unless the cache is explicitly updated with the "set(key, value)" method.**
        
        If the cache does not exist, returns None.
        :param key: key to search.
        """
        value_serialized = self.db.get(key, None)
        if value_serialized is None:
            return None
        value = pickle.loads(value_serialized)
        return value

    def set(self, key: str, value) -> None:
        """
        Sets the cache indexed by key.
        :param key: key to update the value.
        :parma value: new cache value.
        """
        value_serialized = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        self.db[key] = value_serialized

    def delete(self, key: str) -> None:
        """
        Deletes the key from the cache.
        :param key: key to delete from the cache.
        """
        del self.db[key]

    def __getitem__(self, key: str) -> any:
        return self.get(key)

    def __setitem__(self, key: str, value) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.delete(key)

    def close(self):
        """
        closes the database file.
        """
        self.db.close()
        self.db = None


@contextmanager
def get_context_cache():
    """
    manages context of the wrapped dbm object,
    so that closing the dbm database can be done automatically,
    when exitting from the "with" statement.
    """
    # pylint: disable-next=redefined-outer-name
    cache = Cache()
    yield cache
    cache.close()


if __name__ == "__main__":
    # executes test codes.
    USER_ID1 = "user_id1"
    USER_ID2 = "user_id2"

    with get_context_cache() as cache:
        if cache[USER_ID1] is not None:
            del cache[USER_ID1]
        if cache[USER_ID2] is not None:
            del cache[USER_ID2]

        assert cache[USER_ID1] is None
        cache[USER_ID1] = (1, 2, 3) # or "cache.set(USER_ID1, (1, 2, 3))"
        assert cache[USER_ID1] == (1, 2, 3) # or "assert cache.get(USER_ID1) == (1, 2, 3)"

        cache[USER_ID2] = {"age": 21}
        assert cache[USER_ID2] == {"age": 21} 
        del cache[USER_ID2] # or "cache.delete(USER_ID2)"
        assert cache[USER_ID2] is None

    with get_context_cache() as cache:
        # the cache persists even when the process is exitted.
        assert cache[USER_ID1] == (1, 2, 3)
        assert cache[USER_ID2] is None

    with get_context_cache() as cache:
        if cache[USER_ID1] is not None:
            del cache[USER_ID1]

        cache[USER_ID1] = []
        window = cache[USER_ID1]
        window.append(1)
        window.append(2)
        window.append(3)
        cache[USER_ID1] = window
        print(cache[USER_ID1])


