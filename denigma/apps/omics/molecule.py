"""Classes describing a molecule.
Consider using the Python OpenBabel bindings to read file formats,
which allows to read more than PDB files.
Use CPK data for each element form the BLu Obelisk Data Repository."""


class Atom(object):
    """Class to store info about an atom."""
    def __init__(self, id=1, symbol='', residue_symbol='', residueid=-1, pos=None):
        self.id = id
        self.symbol = symbol
        self.residue_symbol = residue_symbol
        self.residueid = residueid
        self.pos = pos or [0,0,0]


class Bond(object):
    """Class to store info about a bond."""
    def __init__(self, atom_id_1=0, atom_id_2=0, type=''):
        self.atom_id_1 = atom_id_1
        self.atom_id_2 = atom_id_2
        self.type = type # single, double or triple.


class Residue(object):
    """Class to store info about a residue."""
    def __init__(self, id=-1, symbol='', atom_ids=None):
        self.id = id
        self.symbol = symbol
        self.atom_ids = atom_ids or []


class Molecule(object):
    """Class to store info about a molecule."""
    def __init__(self, id=0, name='', atoms=None, bonds=None, residues=None):
        self.id = id
        self.name = name
        self.atoms = atoms or {}
        self.bonds = bonds or []
        self.residues = residues or {}

    def __repr__(self):
        string = ["%s Molecule" % self.name]
        for k, v in m.atoms.items():
            string.append("Atom #%s is %s \t x: %.3f \t y: %.3f \t z: %.3f"\
                  % (v.id, v.symbol, v.pos[0], v.pos[1], v.pos[2]))
        for bond in self.bonds:
            string.append("%s bond between atom %s and atom %s"\
                  % (bond.type, bond.atom_id_1, bond.atom_id_2))
        return "\n".join(string)

    def center_and_size(self):
        """Center the molecule about the origin and calculate its size.
        1. Find the highest and lowest atom values for the x,y and z coordinates.
        2. Find the average of the high and low values for each coordinate.
        3. The average * (-1) in each axis is how far we need to move each atom to center the molecule."""
        initialized = False

        # 1.
        for key in self.atoms.keys():
            a = self.atoms[key]
            if not initialized:
                # Initilialize values
                x_high = a.pos[0]
                x_low = a.pos[0]
                y_high = a.pos[1]
                y_low = a.pos[1]
                z_high = a.pos[2]
                z_low = a.pos[2]
                initialized = True
            if a.pos[0] > x_high: x_high = a.pos[0]
            if a.pos[0] < x_low: x_low = a.pos[0]
            if a.pos[1] > y_high: y_high = a.pos[1]
            if a.pos[1] < y_low: y_low = a.pos[1]
            if a.pos[2] > z_high: z_high = a.pos[2]
            if a.pos[2] < z_low: z_low = a.pos[2]

        # 2.
        average_x = (x_high + x_low) / 2
        average_y = (y_high + y_low) / 2
        average_z = (z_high + z_low) / 2

        # 3.
        for key in self.atoms.keys():
            a = self.atoms[key]
            a.pos[0] += -1 * average_x
            a.pos[1] += -1 * average_y
            a.pos[2] += -1 * average_z

        # 4.
        size_x = x_high - x_low
        size_y = y_high - y_low
        size_z = z_high - z_low

        if (size_x >= size_y) and (size_x >= size_z):
            self.size = size_x
        if (size_y >= size_x) and (size_y >= size_z):
            self.size = size_y
        if (size_z > size_y) and (size_z >= size_x):
            self.size = size_z


if __name__ == '__main__':
    m = Molecule(id=1, name="Water")
    m.atoms[1] = Atom(id=1, symbol='O', pos=[1,2,3])
    m.atoms[2] = Atom(id=2, symbol='H', pos=[4,2,3])
    m.atoms[3] = Atom(id=3, symbol='H', pos=[1,5,7])
    for k, v in [(1,2), (1,3)]:
        m.bonds.append(Bond(atom_id_1=k, atom_id_2=v, type='single'))
    print m
        
