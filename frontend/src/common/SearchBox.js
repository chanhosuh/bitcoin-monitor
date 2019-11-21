import React from "react";

class SearchBox extends React.Component {
  state = {
    searchString: ""
  };

  onChange = event => {
    const searchString = event.target.value;
    this.setState({ searchString });
    if (!searchString) {
      this.props.onClear();
    }
  };

  getSearchResults = event => {
    event.preventDefault();
    const searchString = this.searchInput.current.value;
    this.props.onSubmit(searchString);
  };

  render() {
    return (
      <form className="search-box" onSubmit={this.getSearchResults}>
        <input
          type="text"
          value={this.state.searchString}
          onChange={this.onChange}
          required
          placeholder="block or transaction hash"
        />
        <button type="submit">
          <i className="fa fa-search"></i>
        </button>
      </form>
    );
  }
}

export default SearchBox;
