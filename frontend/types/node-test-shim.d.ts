declare module "node:test" {
  type TestFunction = (name: string, fn: () => void | Promise<void>) => void;
  const test: TestFunction;
  export default test;
}

declare module "node:assert/strict" {
  export function equal<T>(actual: T, expected: T, message?: string): void;
  export function deepEqual<T>(actual: T, expected: T, message?: string): void;

  const assert: {
    equal: typeof equal;
    deepEqual: typeof deepEqual;
  };

  export default assert;
}

declare const console: {
  log: (...args: unknown[]) => void;
};
