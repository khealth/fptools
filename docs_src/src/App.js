import React from "react";
import docs from "./docs.json";
import Navigation from "./navigation";
import { getFullName, getLink } from "./util";
import "./App.css";

const Doc = ({ module, name, type, doc, signature, members }) => {
  const fullName = getFullName({ name, module, type });
  return (
    <div className={"item " + type}>
      <a id={fullName} href={getLink(fullName)}>
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

const App = () => (
  <div className="App">
    <Navigation docs={docs} />
    <main>
      {docs.members.map(doc => (
        <Doc key={doc.name} {...doc} />
      ))}
    </main>
  </div>
);

export default App;
