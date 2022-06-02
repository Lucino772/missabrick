import { h } from './bower/preact/index.js'
import register from './bower/preact-custom-element/index.js'
import htm from './bower/htm/index.js'

const html = htm.bind(h)

const Greeting = ({ name = 'World' }) => (
  html`<p>Hello, ${name}!</p>`
);

register(Greeting, 'x-greeting', ['name']);