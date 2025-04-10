import prettierPlugin from "eslint-plugin-prettier";
import vuePlugin from 'eslint-plugin-vue';
import typescriptPlugin from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';
import vueParser from 'vue-eslint-parser';
import pugPlugin from 'eslint-plugin-pug';

/** @type {import('eslint').Linter.FlatConfig[]} */
export default [
  {
    ignores: ['node_modules/**', 'dist/**', '.nuxt/**', '.output/**', '*.config.js', '*.config.ts'],
  },
  {
    files: ['**/*.vue'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: vueParser,
        ecmaVersion: 2021,
        sourceType: 'module',
        extraFileExtensions: ['.vue'],
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    plugins: {
      prettier: prettierPlugin,
      vue: vuePlugin,
      pug: pugPlugin,
    },
    rules: {
      'prettier/prettier': ['error', { 'usePrettierrc': true }],
      'vue/multi-word-component-names': 'off',
      'vue/html-indent': 'off',
      'vue/html-self-closing': 'off',
      'pug/no-multiple-template-root': 'off',
    },
  },
  {
    files: ['**/*.{js,ts}'],
    languageOptions: {
      parser: typescriptParser,
      ecmaVersion: 2021,
      sourceType: 'module',
    },
    plugins: {
      prettier: prettierPlugin,
      '@typescript-eslint': typescriptPlugin,
    },
    rules: {
      'prettier/prettier': ['error', { 'usePrettierrc': true }],
      '@typescript-eslint/no-unused-vars': 'warn',
    },
  },
];
