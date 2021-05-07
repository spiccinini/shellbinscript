#!/usr/bin/env python3

#  Copyright 2021 Santiago Piccinini <spiccinini@altermundi.net>
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import os
import subprocess
import tempfile

def create(indir, outfile):
    script = """set -x
    tmpdir=$(mktemp -d)

    # unpack
    tail -cTAR_SIZE "$0" | tar xvfz - -C ${tmpdir}

    test -e "${tmpdir}/run.sh" && cd ${tmpdir} && sh run.sh
    exit
    """    

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_tar_name = os.path.join(tmpdirname, "data.tar.gz")
        subprocess.run(["tar", "cfz", tmp_tar_name, "-C", indir, "."])

        with open(tmp_tar_name, "rb") as tar:
            tar_data = tar.read()

        with open(outfile, "wb") as outfile:
            script = script.replace("TAR_SIZE", str(len(tar_data)))
            outfile.write(script.encode("ascii"))
            outfile.write(tar_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        Creates a shell installer that embeds a tar file from an input directory.
        If a run.sh script is present in the input directory it will be executed by the installer
        script.
    """)
    parser.add_argument('inputdir', help='Input directory.')
    parser.add_argument('outfile', help='Output installer script (eg: installer.sh).')
    args = parser.parse_args()
    
    create(args.inputdir, args.outfile)
