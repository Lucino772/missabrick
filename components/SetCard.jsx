const SetCard = ({ title = 'This is a set', theme = 'Theme', num_parts = 540, year = 2000, description = "lorem ipsum" }) => {
    return (
        <div class="flex flex-row py-4 gap-4">
            <img class="w-20 h-20 rounded-xl object-cover border border-white" src="https://img.redbull.com/images/c_limit,w_1500,h_1000,f_auto,q_auto/redbullcom/2022/1/28/jnuookfhjrooziqpigvq/lego-art" alt="" />
            <div class="flex-1 flex flex-col">
                <a href="#" class="text-xl font-bold ">9493-1 : Le retour du Jedi</a>
                <span class="text-base font-medium text-slate-600">Star Wars - 540 parts - 1998</span>
            </div>
        </div>
    )
}

export default SetCard;