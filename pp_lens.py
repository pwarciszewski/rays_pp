import numpy as np
import matplotlib.pyplot as plt


def get_m_thin_lens(f):
    return np.array([[1, 0], [-1 / f, 1]])


def get_m_distance(d):
    return np.array([[1, d], [0, 1]])


class lens:
    def __init__(self, focal_length, position):
        self.f = focal_length
        self.x = position


class lab_space:
    def __init__(self):
        self.lens_list = []

    def add_lens(self, f, position):
        self.lens_list.append(lens(f, position))

    def get_transfer_matrix(self):
        ordered_lens_list = sorted(self.lens_list, key=lambda l: l.x)
        transfer_matrix = np.array([[1, 0], [0, 1]])

        for i, item in enumerate(ordered_lens_list):
            transfer_matrix = np.matmul(get_m_thin_lens(item.f), transfer_matrix)
            if i + 1 < len(ordered_lens_list):
                transfer_matrix = np.matmul(
                    get_m_distance(ordered_lens_list[i + 1].x - item.x), transfer_matrix
                )
        return transfer_matrix

    def get_back_pp_parameters(self):
        # returns lab frame position of a back focal point, back principle plane and front back distance
        # back of a lens is a space after the last lens counted from left
        last_lens_postion = sorted(self.lens_list, key=lambda l: l.x)[-1].x

        transfer_matrix = self.get_transfer_matrix()
        transfered_vector = np.matmul(transfer_matrix, np.array([[1], [0]]))
        focal_point_distance = -1 * transfered_vector[0][0] / transfered_vector[1][0]
        focal_point_position = last_lens_postion + focal_point_distance
        pp_position = focal_point_position - self.get_effl()
        return focal_point_position, pp_position, focal_point_distance

    def get_front_pp_parameters(self):
        # returns lab frame position of a front focal point, front principle plane and front focal distance
        first_lens_postion = sorted(self.lens_list, key=lambda l: l.x)[0].x

        transfer_matrix = self.get_transfer_matrix()
        transfer_matrix = np.linalg.inv(transfer_matrix)
        transfered_vector = np.matmul(transfer_matrix, np.array([[1], [0]]))
        focal_point_distance = transfered_vector[0][0] / transfered_vector[1][0]
        focal_point_position = first_lens_postion - focal_point_distance
        pp_position = focal_point_position + self.get_effl()
        return focal_point_position, pp_position, focal_point_distance

    def get_effl(self):
        return -1 / self.get_transfer_matrix()[1][0]

    def show(self):
        plt.axhline(0, color="k")
        for lens in self.lens_list:
            if lens.f > 0:
                plt.axvline(lens.x, color="r")
                plt.text(
                    lens.x,
                    0.01,
                    "f: %.1f" % lens.f,
                    rotation=90,
                    verticalalignment="center",
                )
            else:
                plt.axvline(lens.x, color="b")
                plt.text(
                    lens.x,
                    0.01,
                    "f: %.1f" % lens.f,
                    rotation=90,
                    verticalalignment="center",
                )

        back_fp, back_pp, _ = self.get_back_pp_parameters()
        front_fp, front_pp, _ = self.get_front_pp_parameters()
        effl = self.get_effl()

        plt.title("Effective focal length: %.3f mm" % effl)
        plt.scatter(back_fp, 0, color="y", label="back focal point")
        plt.scatter(front_fp, 0, color="c", label="front focal point")
        plt.axvline(back_pp, color="y", linestyle="dashed", label="back PP")
        plt.axvline(front_pp, color="c", linestyle="dashed", label="front PP")
        plt.xlabel("Postion [mm]")
        plt.yticks([])
        plt.legend()
        plt.show()
