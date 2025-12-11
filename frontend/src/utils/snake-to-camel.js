export default function snake2camel(obj) {
  const convertKey = (key) => {
    return key.replace(/_([a-z])/g, (_, seg) => seg.toUpperCase());
  };

  if (typeof obj === "object" && Array.isArray(obj)) {
    return obj.map((item) => snake2camel(item));
  }

  if (typeof obj === "object" && obj !== null) {
    const ret = {};
    for (const [key, val] of Object.entries(obj)) {
      const camelKey = convertKey(key);
      ret[camelKey] = val;
    }
    return ret;
  }

  return obj;
}
