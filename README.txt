Programming Challenge:

Take a variable number of identically structured json records and de-duplicate the set.

 

An example file of records is given in the accompanying 'leads.json'.  Output should be same format, with dups reconciled according to the following rules:

1. The data from the newest date should be preferred.

2. Duplicate IDs count as dups. Duplicate emails count as dups. Both must be unique in our dataset. Duplicate values elsewhere do not count as dups.

3. If the dates are identical the data from the record provided last in the list should be preferred.

Simplifying assumption: the program can do everything in memory (don't worry about large files).

----------------------------------------------------------------------------------------------------------

The code is structured as follows:

A Class object houses the loaded data, a dictionary of all final emails so far, a dictionary of final ids so far, and a final_elements field showing which elements are in our final response as t/f index list.

When the input json is processed, it does the following:

process_file()
for each item
    if item has a conflict with current final id or email
        remove old conflicts from from final elements t/f list
    add current item to final email and id dictionaries and mark as t in index list

once the final_elements t/f index is generated, we use it to generate our final json structure and write it to a file.

generate_file(output_loc)
    output []
    for index in t/f index:
        if true:
            add to output
    write output object into output_loc file
    
Because we work through the elements linearly, conflicts can be handled sequentially, allowing for O(N) time complexity. Due to use of dictionaries, lookup time in the event of a conflict is O(1).
Space complexity is O(N) due to loading the entire json into memory. 

-------------------------------------------------------------------------------------------

My implementation makes the assumption that at any given time, there should be only one instance of any ID and any email. If a conflict is encountered, the previous element is removed from the final output entirely. The previous id and email are then available for use again. 
My implementation also makes the assumption that elements are given in the json in order of entryDate. Further implementation could be added during the Class init to sort by Datetime if elements are not given in order.

See the following scenarios:
- id exclusive conflict then conflict with old email
[
    {
        id:apple,
        email:foo@bar.com,
    },
    {
        id:apple,
        email:coo@bar.com,
    },
    {
        id:banana,
        email:foo@bar.com,
    },
]
in this example, the element with id banana DOES NOT encounter a conflict and the final output contains elements 2 and 3.


- id exclusive conflict then conflict with new email         - expect conflict with new email
[
    {
        id:apple,
        email:foo@bar.com,
    },
    {
        id:apple,
        email:coo@bar.com,
    },
    {
        id:banana,
        email:coo@bar.com,
    },
]
in this example, the element with id banana DOES encounter a conflict and the final output contains only element 3.


- email exclusive conflict then conflict with old id         - expect no conflict with old id
[
    {
        id:apple,
        email:foo@bar.com,
    },
    {
        id:banana,
        email:foo@bar.com,
    },
    {
        id:apple,
        email:coo@bar.com,
    },
]
in this example, the element with id apple DOES NOT encounter a conflict and final output contains element 2 and 3.


- email exclusive conflict then conflict with new id         - expect conflict with new id
[
    {
        id:apple,
        email:foo@bar.com,
    },
    {
        id:banana,
        email:foo@bar.com,
    },
    {
        id:banana,
        email:coo@bar.com,
    },
]
in this example, the element with id banana DOES encounter a conflict, and the output contains only element 3.


- one new entry conflicts with an email AND an id   - expects both old conflicts to be removed
[
    {
        id:apple,
        email:foo@bar.com,
    },
    {
        id:banana,
        email:coo@bar.com,
    },
    {
        id:banana,
        email:foo@bar.com,
    },
]
in this example, the third element DOES encounter a conflict and the final output contains only element 3.

-----------------------------------------

