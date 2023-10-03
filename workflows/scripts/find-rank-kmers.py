#! /usr/bin/env python
import sys
import argparse
import sourmash

from sourmash.lca.lca_utils import zip_lineage
from sourmash import MinHash, SourmashSignature


def _create_minhash(db):
    is_protein = False
    is_hp = False
    is_dayhoff = False
    if db.moltype == 'protein':
        is_protein = True
    elif db.moltype == 'hp':
        is_hp = True
    elif db.moltype == 'dayhoff':
        is_dayhoff = True

    minhash = MinHash(n=0, ksize=db.ksize, scaled=db.scaled,
                      is_protein=is_protein, hp=is_hp, dayhoff=is_dayhoff)
    return minhash


def main():
    p = argparse.ArgumentParser()
    p.add_argument('lca_db')
    p.add_argument('keep_rank', help="Keep the rank specified (i.e. Species)")
    p.add_argument('-o', '--output', help="output signature containing rank-specific hash values", required=True)
    p.add_argument('-s', '--save-names', help="save list of matching signature names from that lineage to this file")
    args = p.parse_args()

    db, ksize, scaled = sourmash.lca.lca_db.load_single_database(args.lca_db)
    print(f"loaded db k={ksize} scaled={scaled} from '{args.lca_db}'")

    # find all relevant lineage IDs (lid)
    matching_lids = set()
    for lineage, lid in db._lineage_to_lid.items():
        for (rank) in lineage:
            if any(taxon.rank == args.keep_rank for taxon in lineage):
                full_lineage = ";".join(zip_lineage(lineage))
                print(f"full lineage lid={lid}: {full_lineage}")
                matching_lids.add(lid)
                break

    # find all matching idx
    matching_idx = set()
    for idx, lid in db._idx_to_lid.items():
        if lid in matching_lids:
            matching_idx.add(lid)

    print(f"found {len(matching_idx)} matching genomes.")

    individual_signatures = []  # Create an empty list to store individual signatures

    for hashval, idx_set in db._hashval_to_idx.items():
        idx_set = set(idx_set)
        if idx_set.issubset(matching_idx):
            # Find the name associated with the matching idx
            name = None
            for ident, idx in db._ident_to_idx.items():
                if idx in idx_set:
                    name = db._ident_to_name[ident]
                    break

            if name:
                #full_lineage = ";".join(zip_lineage(lineage))  # Get full lineage as a string
                mh = _create_minhash(db)
                mh.add_hash(hashval)  # Use add_hash method to add a single hash value
                ss = SourmashSignature(mh, name=f"{name}, Kept Rank: {args.keep_rank}")  # Use the name
                individual_signatures.append(ss)

#            ss = SourmashSignature(mh, name=f"{name}, {full_lineage}, Lineage: {args.keep_rank}")

    with open(args.output, "wt") as fp:
        sourmash.save_signatures(individual_signatures, fp)

    print(f"Saved signatures to '{args.output}'")

    if args.save_names:
        print(f"saving matching signature names to '{args.save_names}'")
        with open(args.save_names, "wt") as fp:
            for ident, idx in db._ident_to_idx.items():
                if idx in matching_idx:
                    name = db._ident_to_name[ident]
                    fp.write(f"{name}\n")
    else:
        print(f"did not save matching names; see --save-names")

if __name__ == '__main__':
    sys.exit(main())

