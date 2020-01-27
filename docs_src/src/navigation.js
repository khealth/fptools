import React, { useState, useCallback } from "react";
import { getFullName, getLink } from "./util";

const NavigationMenuItem = ({ module, doc, filter }) => {
  const fullName = getFullName({ ...doc, module });
  const href = getLink(fullName);
  const active = window.location.hash === href;
  const isModule = doc.type === "module";
  if (filter && !isModule && !doc.name.includes(filter)) {
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

  const Tag = isModule ? "h5" : "span";

  return (
    <li>
      <Tag className={active ? "active" : ""}>
        <a href={href}>{nameNode}</a>
      </Tag>
      {doc.members && (
        <NavigationMenu
          module={doc.name}
          members={doc.members}
          filter={doc.name.includes(filter) ? "" : filter}
        />
      )}
    </li>
  );
};

const NavigationMenu = ({ module, members, filter }) => (
  <ul>
    {members.map(doc => {
      return (
        <NavigationMenuItem
          key={doc.name}
          module={module}
          doc={doc}
          filter={filter}
        />
      );
    })}
  </ul>
);

const Navigation = ({ docs }) => {
  const [query, setQuery] = useState("");
  const handleChange = useCallback(
    event => {
      setQuery(event.target.value);
    },
    [setQuery]
  );
  return (
    <nav>
      <h3>{docs.name}</h3>
      <input
        type="search"
        value={query}
        onChange={handleChange}
        autoFocus={window.location.hash === ""}
      />
      <NavigationMenu members={docs.members} filter={query} />
    </nav>
  );
};

export default Navigation;
