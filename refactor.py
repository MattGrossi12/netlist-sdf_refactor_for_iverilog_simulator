from pathlib import Path
import re

class RefatoradorDeNomes:
    def cprint(self, mensagem):
        """
        Função de print customizada. Se você não tiver uma,
        pode simplesmente usar 'print(mensagem)' ou adaptar.
        No script original, self.cprint é usado, então precisamos defini-la.
        """
        print(mensagem)

from pathlib import Path
import re

from pathlib import Path
import re

class RefatoradorDeNomes:
    def cprint(self, msg):
        print(msg)

    def _pick_from_cwd(self, patterns, kind, required=False):
        cwd = Path.cwd()

        all_candidates = []
        seen = set()
        for pat in patterns:
            for p in cwd.glob(pat):
                if p.is_file():
                    rp = str(p.resolve())
                    if rp not in seen:
                        seen.add(rp)
                        all_candidates.append(p)

        if not all_candidates:
            if required:
                self.cprint(f"ERRO: Nenhum arquivo {kind} encontrado na pasta atual: {cwd}")
            return None

        # respeita preferência dos patterns; desempate: mais recente
        chosen = None
        for pat in patterns:
            subset = [p for p in all_candidates if p.match(pat)]
            if subset:
                subset.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                chosen = subset[0]
                break

        if chosen is None:
            all_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            chosen = all_candidates[0]

        if len(all_candidates) > 1:
            others = [p.name for p in all_candidates if p.resolve() != chosen.resolve()]
            self.cprint(
                f"AVISO: Vários arquivos {kind} encontrados. Usando '{chosen.name}'. "
                f"Outros: {', '.join(others)}"
            )
        else:
            self.cprint(f"Usando {kind}: '{chosen.name}'")

        return chosen

    def refactor_generated_names(self, i_netlist=None, i_sdf=None):
        # ---------------- Resolver NETLIST (opcional) ----------------
        netlist_path = None
        if i_netlist and str(i_netlist).strip():
            p = Path(i_netlist)
            if p.exists():
                netlist_path = p
            else:
                alt = Path.cwd() / p.name
                if alt.exists():
                    self.cprint(f"AVISO: '{i_netlist}' não encontrado; usando '{alt.name}' na pasta atual.")
                    netlist_path = alt
                else:
                    self.cprint(f"AVISO: Netlist '{i_netlist}' não encontrado. Pulando refatoração do netlist.")
                    netlist_path = None
        else:
            # auto-detect (opcional): preferir *.nl.v, depois *.v
            netlist_path = self._pick_from_cwd(["*.nl.v", "*.v"], "netlist Verilog (.v)", required=False)

        # ---------------- REFACTOR NETLIST (se existir) ----------------
        refactor_netlist_path = None
        if netlist_path is not None:
            try:
                with open(netlist_path, "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                self.cprint(f"AVISO: Arquivo netlist '{netlist_path}' não encontrado. Pulando netlist.")
            else:
                newlist_net = []
                for line in lines:
                    if "\\" in line:
                        self.cprint("--[refactor_generated_names] before," + str(line.strip()))
                        line = re.sub(r"\]\.", r"__", line)
                        line = re.sub(r"\]", r"_", line)
                        line = re.sub(r"\[", r"_", line)
                        line = re.sub(r"([0-9a-zA-Z])\.([0-9a-zA-Z])", r"\1__\2", line)
                        line = re.sub(r"\\blk", r"blk", line)
                        line = re.sub(r"\\", r"", line)
                        self.cprint("----[refactor_generated_names] after," + str(line.strip()))
                    newlist_net.append(line)

                refactor_netlist_path = Path(
                    netlist_path.parent,
                    netlist_path.stem.replace(".", "_") + "_refactor.v",
                )
                with open(refactor_netlist_path, "w", newline="\n") as f:
                    f.writelines(newlist_net)
                self.cprint("------[refactor_generated_names] write to " + str(refactor_netlist_path))
        else:
            self.cprint("------[refactor_generated_names] Nenhum netlist encontrado/fornecido. Pulando refatoração do netlist.")

        # ---------------- Resolver SDF (opcional) ----------------
        sdf_path = None
        if i_sdf and str(i_sdf).strip():
            p = Path(i_sdf)
            if p.exists():
                sdf_path = p
            else:
                alt = Path.cwd() / p.name
                if alt.exists():
                    self.cprint(f"AVISO: '{i_sdf}' não encontrado; usando '{alt.name}' na pasta atual.")
                    sdf_path = alt
                else:
                    self.cprint(f"AVISO: SDF '{i_sdf}' não encontrado. Pulando refatoração do SDF.")
                    sdf_path = None
        else:
            sdf_path = self._pick_from_cwd(["*.sdf"], "SDF (.sdf)", required=False)

        # ---------------- REFACTOR SDF (se existir) ----------------
        refactor_sdf_path = None
        if sdf_path is not None:
            try:
                with open(sdf_path, "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                self.cprint(f"AVISO: Arquivo SDF '{sdf_path}' não encontrado. Pulando SDF.")
            else:
                newlist_sdf = []
                for line in lines:
                    if "\\" in line:
                        print("--[SDF] before," + str(line.strip()))
                        line = re.sub(r"\\\]\\\.", r"__", line)
                        line = re.sub(r"\\\]", r"_", line)
                        line = re.sub(r"\\\[", r"_", line)
                        line = re.sub(r"([0-9a-zA-Z])\\\.([0-9a-zA-Z])", r"\1__\2", line)
                        print("----[SDF] after," + str(line.strip()))
                    newlist_sdf.append(line)

                refactor_sdf_path = Path(
                    sdf_path.parent,
                    sdf_path.stem.replace(".", "_") + "_refactor.sdf",
                )
                with open(refactor_sdf_path, "w", newline="\n") as f:
                    f.writelines(newlist_sdf)
                self.cprint("------[refactor_generated_names] write to " + str(refactor_sdf_path))
        else:
            self.cprint("------[refactor_generated_names] Nenhum SDF encontrado/fornecido. Pulando refatoração do SDF.")

        return refactor_netlist_path, refactor_sdf_path


if __name__ == "__main__":
    ferramenta = RefatoradorDeNomes()

    # Ambos opcionais agora:
    # - Se existir *.nl.v/*.v e/ou *.sdf na pasta atual, ele processa.
    # - Se não existir, ele só avisa e termina sem erro.
    path_netlist_refatorada, path_sdf_refatorado = ferramenta.refactor_generated_names(None, None)

    if path_netlist_refatorada:
        print(f"\nArquivo Verilog (.v) modificado foi salvo em: {path_netlist_refatorada}")
    if path_sdf_refatorado:
        print(f"Arquivo SDF (.sdf) modificado foi salvo em: {path_sdf_refatorado}")

    print("\nProcesso concluído.")