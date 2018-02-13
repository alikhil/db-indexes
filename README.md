# DropSQL indexes

1. Why we can use only standard libs?
2. What types should be able to indexed?
3. What kind of operations should be supported by our indexes?
4. Does dropsql support indexes by design?

## Steps

1. Implement b-tree, bitmap and hash indexes by inheriting `AbstractIndex` and implementing abstract methods
2. Redesign index implementations to integrate them into dropsql


## Testing indexes

