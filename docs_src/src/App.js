import React, { Component, useState } from "react";
import docs from "./docs.json";
import "./App.css";

const NavigationMenu = ({ module, members, filter }) => (
  <ul>
    {members.map(doc => {
      if (filter && !doc.members && !doc.name.includes(filter)) {
        return null;
      }
      const nameNode = !filter || !doc.name.includes(filter) ? doc.name : doc.name.split(filter).map((part, i, array) => {
        if (i < array.length - 1) {
          return [part, <b>{filter}</b>]
        }
        return part
      })
      return (
        <li>
          <a href={"#" + getFullName({ ...doc, module })}>{nameNode}</a>
          {doc.members && (
            <NavigationMenu
              module={doc.name}
              members={doc.members}
              filter={filter}
            />
          )}
        </li>
      );
    })}
  </ul>
);

const Navigation = ({ docs }) => {
  const [query, setQuery] = useState("");
  return (
    <nav>
      <input
        type="search"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <ul>{<NavigationMenu members={docs.members} filter={query} />}</ul>
    </nav>
  );
};

const getFullName = ({ name, module, type }) =>
  type === "module"
    ? name
    : module + "." + name + (type === "function" ? "()" : "");

const Doc = ({ module, name, type, doc, signature, is_pkg, members }) => {
  const fullName = getFullName({ name, module, type });
  return (
    <div className={type}>
      <a id={fullName} href={"#" + fullName}>
        <h5>{fullName}</h5>
      </a>
      {signature && <pre>{signature}</pre>}
      <p>{doc}</p>
      {members &&
        members.map(member => (
          <Doc key={member.name} module={name} {...member} />
        ))}
    </div>
  );
};

class App extends Component {
  render() {
    return (
      <div className="App">
        <Navigation docs={docs} />
        <main>
          <Doc {...docs} />
        </main>
      </div>
    );
  }
}

export default App;
