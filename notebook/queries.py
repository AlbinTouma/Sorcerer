from pandas import DataFrame

def create_queries(df: DataFrame) -> DataFrame:

    four_trenches = {"quality, age, name, occupation": len(df[(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)])}
    
    three_trenches = {
            "quality,age, occupation": len(
                df[(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)],
                ),
            "quality,age, name": len(
                df[(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)],
                ),
            "quality, name, occupation": len(
                df[(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)],
                ),       
            "age, name, occupation": len(
                df[~(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)]),   
        }
    
    
    
    two_trenhces = {
            "quality, age": len(
                df[(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)]),
            "quality, occupation": len(
                df[(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)]),
            "age, name": len(
                df[~(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)]),
            "quality, name": len(
                df[(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)]),          
            "name, occupation": len(
                df[~(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)]),
            "age, occupation": len(
                df[~(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)]),
        }
    
    
    one_trench = {
            "age": len(
                df[~(df['score.data_quality'] < 0.5 ) & (df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)]),
            "occupation": len(
                df[~(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & (df['has_occupation'] == False)]),     
            "quality": len(
                df[(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & ~(df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)]),
            "name": len(
                df[~(df['score.data_quality'] < 0.5 ) & ~(df['score.age'] == 0) & (df['TOTAL_FLAGS'] > 0) & ~(df['has_occupation'] == False)]),
    }




    '''
    Creates the queries needed to break data into trenches based on the conditions they break
    '''
    result_dict = {**four_trenches, **three_trenches, **two_trenhces, **one_trench}
    result = DataFrame.from_dict(result_dict, orient='index', columns=['count']).reset_index()
    result.loc[0, 'Tranche'] = 4
    result.loc[1, 'Tranche'] = 3
    result.loc[5, 'Tranche'] = 2
    result.loc[11, 'Tranche'] = 1
    result['Tranche'] = result['Tranche'].fillna('')
    result = result.set_index('Tranche')
    result['quality'] = ['x', 'x', 'x', 'x', '', 'x', 'x', '', 'x', '', '', '', '', 'x', '']
    result['age'] = ['x', 'x', 'x', '', 'x', 'x', '', 'x', '', '', 'x', 'x', '', '', '']
    result['name'] = ['x', '', 'x', 'x', 'x', '', '', 'x', 'x', 'x', '', '', '', '', 'x']
    result['occupation'] = ['x', 'x', '', 'x', 'x', '', 'x', '', '', 'x', 'x', '', 'x', '', '']
    return result



    
    