import axios from "axios";

import { useState } from "preact/hooks";
import { useConfirmUnload } from "./hooks/useConfirmUnload";

import { SpinnerIcon, UploadIcon } from "./icons";

const UploadButton = ({ multiple = false }) => {
    const setConfirmUnload = useConfirmUnload();

    const [loading, setLoading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(-1); 
    const [text, setText] = useState("Upload");

    const onChange = (e) => {
        let formData = new FormData();

        for (let i = 0; i < e.target.files.length; i++) {
            const _file = e.target.files[i];
            formData.append('file', _file, _file.name)
        }

        setLoading(true);
        setConfirmUnload(true);
        axios.post("/upload", formData, {
            onUploadProgress: (pe) => {
                const progress = Math.round((pe.loaded / pe.total) * 100);
                if (text !== "Uploading...")
                    setText("Uploading...")
                if (progress !== 100)
                {
                    setUploadProgress(progress);
                }
                else
                {
                    setUploadProgress(-1);
                    setText("Processing...")
                }
            },
        })
            .then(res => {
                setText("Upload");
                setUploadProgress(-1);
                setLoading(false);
                setConfirmUnload(false);

                // TODO: open window
            })
            .catch(err => {
                setText("Upload")
                setUploadProgress(-1);
                setLoading(false);
                setConfirmUnload(false);
            })
    }

    return (
        <label for="upload-button" class="hover:cursor-pointer">
            <div class="transition relative flex flex-row items-center gap-2 bg-orange-700 hover:bg-orange-700/90 px-3 py-2 border border-orange-700 rounded">
                {loading && <SpinnerIcon text={uploadProgress !== -1 ? `${uploadProgress}` : ''} />}
                {!loading && <UploadIcon />}
                <span class="font-semibold text-base text-white">{text}</span>
            </div>
            <input id="upload-button" type="file" class="hidden" disabled={loading} onChange={onChange} multiple={multiple} />
        </label>
    )
}

export default UploadButton;