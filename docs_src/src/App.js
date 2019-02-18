import React, { Component, useState } from "react";
import docs from "./docs.json";
import "./App.css";

const NavigationMenu = ({ module, members, filter }) => (
  <ul>
    {members.map(doc => {
      if (filter && !doc.members && !doc.name.includes(filter)) {
        return null;
      }
      const nameNode =
        !filter || !doc.name.includes(filter)
          ? doc.name
          : doc.name.split(filter).map((part, i, array) => {
              if (i < array.length - 1) {
                return [part, <b key={i}>{filter}</b>];
              }
              return part;
            });
      const Tag = doc.members ? "h5" : "span";
      return (
        <li key={doc.name}>
          <Tag>
            <a href={"#" + getFullName({ ...doc, module })}>{nameNode}</a>
          </Tag>
          {doc.members && (
            <NavigationMenu
              module={doc.name}
              members={doc.members}
              filter={doc.name.includes(filter) ? '' : filter}
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
      <h3>{docs.name}</h3>
      <input
        type="search"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <NavigationMenu members={docs.members} filter={query} />
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
    <div className={"item " + type}>
      <a id={fullName} href={"#" + fullName}>
        {type === "module" ? (
          <h4>{name}</h4>
        ) : (
          <pre>
            {signature ? (
              <>
                {module && module + "."}
                <b>{name}</b>
                {signature}
              </>
            ) : (
              <>
                {module && module + "."}
                <b>{name}</b>
              </>
            )}
          </pre>
        )}
      </a>
      {doc && <p>{doc}</p>}
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
          {docs.members.map(doc => (
            <Doc key={doc.name} {...doc} />
          ))}
        </main>
      </div>
    );
  }
}

export default App;
