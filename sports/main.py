import service.over_under as ou
import view.build_view as view


def over_under():
    results = ou.over_under()
    return results
    # view.build_page(results)
    # for result in results:
    #     print(result)


if __name__ == '__main__':
    over_under()
