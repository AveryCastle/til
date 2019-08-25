# JEST Practice

- yarn init
- yarn add --dev jest
- yarn add --dev babel-jest @babel/core @babel/preset-env
- Configure Bable
  ```
    // babel.config.js
    module.exports = {
      presets: [
        [
          '@babel/preset-env',
          {
            targets: {
              node: 'current',
            },
          },
        ],
      ],
    };
  ```
- yarn test -o --watch
