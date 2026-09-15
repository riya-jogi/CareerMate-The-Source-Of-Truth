declare module 'mammoth/mammoth.browser' {
  const mammoth: {
    extractRawText: (options: { arrayBuffer: ArrayBuffer }) => Promise<{ value: string }>;
  };

  export default mammoth;
}
