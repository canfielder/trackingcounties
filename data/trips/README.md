# Trips

Trip logs used to batch-enter county visits into `data/tables/list_of_counties_active.csv`.

## Naming convention

`YYYY-MM-DD__short-description.md` — date is the first day of the trip.

## File format

```markdown
# Trip Overview
## Summary
- Brief description of the trip

**States:** State1, State2

## Counties
### YYYY-MM-DD
* County, ST
* County, ST

### YYYY-MM-DD
* County, ST
```

## Workflow

1. Create a trip file here using the naming convention above.
2. List every county visited, grouped by date.
3. Update `data/tables/list_of_counties_active.csv` for each new county:
   - Set `date` to the county's **first appearance** in the trip log.
   - Add a short `notes` entry referencing the trip or event.
   - Skip counties that already have a date recorded.
