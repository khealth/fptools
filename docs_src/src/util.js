export const getFullName = ({ name, module, type }) =>
  type === "module"
    ? name
    : module + "." + name + (type === "function" ? "()" : "");

export const getLink = fullName => "#" + fullName;
