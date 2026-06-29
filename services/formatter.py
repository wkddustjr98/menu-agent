class Formatter:

    def format(self, menus):

        result = []

        for m in menus:

            result.append({

                "course": m.get("COURSE_NAME", ""),
                "main": m.get("MENU_NAME", ""),
                "sides": [
                    m.get("SIDE_1", ""),
                    m.get("SIDE_2", ""),
                    m.get("SIDE_3", ""),
                    m.get("SIDE_4", ""),
                    m.get("SIDE_5", ""),
                    m.get("SIDE_6", "")
                ],
                "kcal": m.get("KCAL", ""),
                "rating": float(m.get("AVG_STAR") or 0),
                "rating_count": int(m.get("SATI_CNT") or 0),
                "origin": m.get("MENU_ORIGIN", ""),
                "soldout": m.get("SOLDOUT_YN", "N") == "Y",
                "congestion": m.get("CONGESTION", ""),
                "guide": m.get("MENU_GUIDE", "")

            })

        return result