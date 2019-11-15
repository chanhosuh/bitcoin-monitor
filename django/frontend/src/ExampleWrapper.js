import React, { Fragment } from "react";
import { FixedSizeList as List } from "react-window";
import InfiniteLoader from "react-window-infinite-loader";
import AutoSizer from "react-virtualized-auto-sizer";

import { Link } from "react-router-dom";

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

  latestBlockHeight
}) => {
  // If there are more items to be loaded then add an extra row to hold a loading indicator.
  const itemCount = hasNextPage ? items.length + 1 : items.length;

  // Only load 1 page of items at a time.
  // Pass an empty callback to InfiniteLoader in case it asks us to load more than once.
  const loadMoreItems = isNextPageLoading ? () => {} : loadNextPage;

  // Every row is loaded except for our loading indicator row.
  const isItemLoaded = index => !hasNextPage || index < items.length;

  // Render an item or a loading indicator.
  const Item = ({ index, style }) => {
    if (!isItemLoaded(index)) {
      return <div style={style}>Loading ... </div>;
    } else {
      const { height, hash, age } = items[index];
      return (
        <div style={style}>
          {height}
          <Link to={`/block/${hash}`}>{hash}</Link>
          {age}
        </div>
      );
    }
  };

  return (
    <Fragment>
      <h2> Current Block: {latestBlockHeight} </h2>
      <AutoSizer>
        {({ height, width }) => (
      <InfiniteLoader
        isItemLoaded={isItemLoaded}
        itemCount={itemCount}
        loadMoreItems={loadMoreItems}
      >
        {({ onItemsRendered, ref }) => (
              <List
                className="List"
                height={height}
                itemCount={itemCount}
                itemSize={30}
                onItemsRendered={onItemsRendered}
                ref={ref}
                width={width}
              >
                {Item}
              </List>
            )}
          </InfiniteLoader>
        )}
          </AutoSizer>
    </Fragment>
  );
};

export default ExampleWrapper;
