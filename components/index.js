import register from "preact-custom-element";

import DownloadSetButton from "./DownloadSetButton";
import UploadButton from "./UploadButton";

register(DownloadSetButton, 'x-download-set-button', ['placeholder'])
register(UploadButton, 'x-upload-set-button', ['multiple'])
