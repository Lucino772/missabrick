import axios from "axios";

const Dropzone = () => {

    const onInput = (e) => {
        console.log(e.target.files)
    }

    return (
        <div class="flex justify-center items-center w-full h-full">
            <label for="dropzone-file" class="flex flex-col justify-center items-center w-full h-full bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer hover:bg-gray-100">
                <div class="flex flex-col justify-center items-center pt-5 pb-6">
                    <svg class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                    <p class="mb-2 text-sm text-gray-500"><span class="font-semibold">Click to upload</span> or drag and drop</p>
                    <p class="text-xs text-gray-500">XLSX, XLS or CSV</p>
                </div>
                <input id="dropzone-file" type="file" class="hidden" onInput={onInput} />
            </label>
        </div>
    )
}

export default Dropzone;