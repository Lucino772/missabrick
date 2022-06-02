import register from "preact-custom-element";

import Dropzone from "./Dropzone";
import SetCard from "./SetCard";

register(Dropzone, 'x-dropzone', [])
register(SetCard, 'x-set-card', ['title', 'theme', 'num_parts', 'year', 'description'])
