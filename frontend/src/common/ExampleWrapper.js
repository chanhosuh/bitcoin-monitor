import React from "react";
import "./ExampleWrapper.css";
import {
  InfiniteLoader,
  List,
  AutoSizer,
  Table,
  Column,
} from "react-virtualized";
import "react-virtualized/styles.css";

const ExampleWrapper = ({
  // Are there more items to load?
  // (This information comes from the most recent API request.)
  hasNextPage,

  // Are we currently loading a page of items?
  // (This may be an in-flight flag in your Redux store for example.)
  isNextPageLoading,

  // Array of items loaded so far.
  items,

  // Callback function responsible for loading the next page of items.
  loadNextPage,

  RowComponent,
}) => {
  // If there are more items to be loaded then add an extra row to hold a loading indicator.
  const itemCount = hasNextPage ? items.length + 1 : items.length;

  // Only load 1 page of items at a time.
  // Pass an empty callback to InfiniteLoader in case it asks us to load more than once.
  const loadMoreItems = isNextPageLoading ? () => {} : loadNextPage;

  // Every row is loaded except for our loading indicator row.
  const isItemLoaded = (index) => !hasNextPage || index < items.length;

  // Render an item or a loading indicator.
  const Item = ({ key, index, style }) => {
    if (!isItemLoaded(index)) {
      return (
        <div key={key} style={style}>
          <div className="loading">Loading</div>
        </div>
      );
    } else {
      const item = items[index];
      return (
        <div
          className={index % 2 ? "ListItemOdd" : "ListItemEven"}
          key={key}
          style={style}
        >
          <RowComponent item={item} />
        </div>
      );
    }
  };

  return (
    <AutoSizer>
      {({ height, width }) => (
        <InfiniteLoader
          isRowLoaded={isItemLoaded}
          rowCount={itemCount}
          loadMoreRows={loadMoreItems}
        >
          {({ onRowsRendered, ref }) => (
            <Table
              width={width}
              height={height}
              rowHeight={35}
              rowCount={itemCount}
              rowSize={50}
              onRowsRendered={onRowsRendered}
              rowRenderer={Item}
              rowGetter={Item}
              headerHeight={35}
              ref={ref}
            >
              <Column flexGrow={1} label="Height" dataKey="height" width={5} />
              <Column width={20} flexGrow={1} label="Time" />
              <Column width={10} flexGrow={1} label="Amount" />
              <Column
                width={10}
                flexGrow={1}
                label="No. of Tx"
                dataKey="num_tx"
              />
              <Column
                width={30}
                flexGrow={1}
                label="Created by"
                dataKey="created_by"
              />
              <Column width={80} flexGrow={1} label="Hash" dataKey="hash" />
            </Table>
          )}
        </InfiniteLoader>
      )}
    </AutoSizer>
  );
};

export default ExampleWrapper;
