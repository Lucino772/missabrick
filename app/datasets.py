import typing
import pandas as pd

class BaseSet:

    def __init__(self, set_num: str) -> None:
        self.__set_num = set_num

    @property
    def set_num(self):
        return self.__set_num

    @property
    def _inventories(self):
        inventories = pd.read_csv('./datasets/inventories.csv')


        all_invs = inventories[inventories['set_num'] == self.__set_num]
        invs = all_invs[all_invs['version'] >= all_invs['version'].max()]

        return invs['id']


class SetsSet(BaseSet):
    
    @property
    def sets(self):
        all_sets_df = pd.read_csv('./datasets/sets.csv')
        inventory_sets_df = pd.read_csv('./datasets/inventory_sets.csv')

        sets = inventory_sets_df[inventory_sets_df['inventory_id'].isin(self._inventories)].filter(items=['set_num', 'quantity'])
        fsets = sets.join(all_sets_df.set_index('set_num'), on=['set_num'])
        
        return fsets

class PartsSet(BaseSet):

    @property
    def parts(self):
        colors_df = pd.read_csv('./datasets/colors.csv').rename(columns={'name': 'color_name', 'rgb': 'color_rgb', 'is_trans': 'color_is_trans'})
        all_parts_df = pd.read_csv('./datasets/parts.csv').rename(columns={'name': 'part_name'})
        inventory_parts_df = pd.read_csv('./datasets/inventory_parts.csv')

        parts = (
            inventory_parts_df[inventory_parts_df['inventory_id'].isin(self._inventories)]
            .filter(items=['part_num', 'color_id', 'quantity', 'is_spare'])
            .join(colors_df.set_index('id'), on=['color_id'])
            .join(all_parts_df.set_index('part_num'), on=['part_num'])
        ).reset_index(drop=True)

        return parts

    @property
    def elements(self):
        elements_df = pd.read_csv('./datasets/elements.csv')

        elements = (
            self.parts.filter(items=['part_num', 'color_id'])
            .join(elements_df.set_index(['part_num', 'color_id']), on=['part_num', 'color_id'])
        ).reset_index(drop=True)

        return elements

class MinifigsSet(BaseSet):

    @property
    def minifigs(self):
        all_minifigs_df = pd.read_csv('./datasets/minifigs.csv')
        inventory_minifigs_df = pd.read_csv('./datasets/inventory_minifigs.csv')

        minifigs = inventory_minifigs_df[inventory_minifigs_df['inventory_id'].isin(self._inventories)].filter(items=['fig_num', 'quantity'])
        fminifigs = minifigs.join(all_minifigs_df.set_index('fig_num'), on=['fig_num'])

        return fminifigs


class Set(SetsSet, PartsSet, MinifigsSet):
    
    def __init__(self, set_num: str, quantity: int = None) -> None:
        super().__init__(set_num)
        self.__quantity = quantity

    @property
    def quantity(self):
        return self.__quantity

    @property
    def sets(self):
        return SetGroup([Set(row['set_num'], row['quantity']) for _, row in super().sets.iterrows()])

    @property
    def parts(self):
        parts = super().parts
        
        if self.__quantity is not None:
            parts['quantity'] = parts['quantity'] * self.__quantity

        return parts

    @property
    def minifigs(self):
        return MinifigGroup([Minifig(row['fig_num'], row['quantity']) for _, row in super().minifigs.iterrows()])

class Minifig(PartsSet):
    
    def __init__(self, fig_num: str, quantity: int = None, parent_set: str = None) -> None:
        super().__init__(fig_num)
        self.__quantity = quantity
        self.__parent_set = parent_set

    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def parts(self):
        parts = super().parts
        
        if self.__quantity is not None:
            parts['quantity'] = parts['quantity'] * self.__quantity

        if self.__parent_set is not None:
            parts['parent_set'] = self.__parent_set

        return parts 


class SetGroup:

    def __init__(self, sets: typing.Iterable['Set']) -> None:
        self.__sets = sets

    def __iter__(self):
        return iter(self.__sets)

    def __len__(self):
        return len(self.__sets)

    @property
    def parts(self):
        parts = []

        for _set in self.__sets:
            set_parts = _set.parts
            set_parts['set_num'] = _set.set_num
            parts.append(set_parts)

        return pd.concat(parts)

    @property
    def elements(self):
        elements = []

        for _set in self.__sets:
            set_elements = _set.elements
            set_elements['set_num'] = _set.set_num
            elements.append(set_elements)

        return pd.concat(elements)

    @property
    def minifigs(self):
        minifigs = []

        for _set in self.__sets:
            for minifig in _set.minifigs:
                minifigs.append(Minifig(minifig.set_num, minifig.quantity, _set.set_num))
        
        return MinifigGroup(minifigs)

class MinifigGroup:

    def __init__(self, minifigs: typing.Iterable['Minifig']) -> None:
        self.__minifigs = minifigs

    def __iter__(self):
        return iter(self.__minifigs)

    def __len__(self):
        return len(self.__minifigs)

    @property
    def parts(self):
        parts = []
        for minifig in self.__minifigs:
            minifig_parts = minifig.parts
            minifig_parts['fig_num'] = minifig.set_num
            parts.append(minifig_parts)

        return pd.concat(parts)

    @property
    def elements(self):
        elements = []

        for _set in self.__sets:
            set_elements = _set.elements
            set_elements['fig_num'] = _set.set_num
            elements.append(set_elements)

        return pd.concat(elements)
