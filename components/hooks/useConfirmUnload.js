import { useEffect, useCallback, useState } from "preact/hooks";

const useConfirmUnload = () => {
    const [block, setBlock] = useState(false);

    const handleBeforeUnload = useCallback((ev) => {
        console.log('BLOCKED', block);
        if (block) {
            ev.preventDefault();
            ev.returnValue = 'Still uploading, are your sure ?';
            return ev.returnValue;
        }
    }, [block]);

    useEffect(() => {
        window.addEventListener('beforeunload', handleBeforeUnload);
        return () => window.removeEventListener('beforeunload', handleBeforeUnload);
    }, [block])

    return setBlock;
}

export { useConfirmUnload };