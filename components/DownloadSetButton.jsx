import axios from "axios";
import { saveAs } from 'file-saver';
import { useCallback, useState } from "preact/hooks";

import { useConfirmUnload } from "./hooks/useConfirmUnload";

import { DownloadIcon, SpinnerIcon } from "./icons";

const DownloadSetButton = ({ placeholder = "Enter value" }) => {
    const setConfirmUnload = useConfirmUnload();

    const [setNumber, setSetNumber] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleInputChange = useCallback((ev) => {
        setSetNumber(ev.target.value);
        setError(null);
    }, [setSetNumber])

    const handleSubmit = useCallback(() => {
        setLoading(true);
        setConfirmUnload(true);
        axios.get(`/set/${setNumber}/file`, {
            responseType: 'blob'
        }).then((res) => {
            const blob = new Blob([res.data], { type: res.headers["content-type"] });
            saveAs(blob, res.headers.filename);
            setLoading(false);
            setConfirmUnload(false);
        }).catch((err) => {
            setError(err.code)
            setLoading(false);
            setConfirmUnload(false);
        });
    }, [setNumber, setLoading, setConfirmUnload, setError]);


    const handleKeyUp = useCallback((ev) => {
        if (ev.keyCode === 13)
            handleSubmit();
    }, [handleSubmit]);

    return (
        <div className="flex flex-col flex-1">
            <div className="flex">
                <input type="text" placeholder={placeholder} value={setNumber} onInput={handleInputChange} onKeyUp={handleKeyUp} className="transition flex-1 font-semibold text-gray-700 rounded-l border-r-0 border-gray-200 focus:ring-0 focus:border-orange-700" />
                <button className="transition-colors bg-orange-700 hover:bg-orange-700/80 w-11 rounded-r flex justify-center items-center" onClick={handleSubmit}>
                    {!loading && <DownloadIcon />}
                    {loading && <SpinnerIcon />}
                </button>
            </div>
            {error !== null && <span className="text-red-600 mt-1 text-sm pl-2">{error}</span>}
        </div>
    );
};

export default DownloadSetButton;